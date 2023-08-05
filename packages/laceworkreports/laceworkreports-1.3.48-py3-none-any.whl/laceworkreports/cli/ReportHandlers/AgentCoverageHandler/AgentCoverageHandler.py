"""
Report Handler
"""

from typing import List as typingList
from typing import Optional

import logging
from datetime import datetime, timedelta
from pathlib import Path

import typer

from laceworkreports import common
from laceworkreports.sdk.DataHandlers import DataHandlerTypes, ExportHandler
from laceworkreports.sdk.ReportHelpers import AgentQueries, ReportHelper

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(no_args_is_help=True, help="Generate HTML report")
def html(
    ctx: typer.Context,
    start_time: datetime = typer.Option(
        (datetime.utcnow() - timedelta(hours=25)).strftime(common.ISO_FORMAT),
        formats=[common.ISO_FORMAT],
        help="Start time for query period",
    ),
    end_time: datetime = typer.Option(
        (datetime.utcnow()).strftime(common.ISO_FORMAT),
        formats=[common.ISO_FORMAT],
        help="End time for query period",
    ),
    subaccounts: bool = typer.Option(
        False,
        help="Enumerate subaccounts",
        envvar=common.LACEWORK_REPORTS_SUBACCOUNTS,
    ),
    file_path: str = typer.Option(
        ...,
        help="Path to exported result",
        envvar=common.LACEWORK_REPORTS_FILE_PATH,
    ),
    template_path: str = typer.Option(
        Path(__file__).resolve().parent.joinpath("agent_coverage.html.j2"),
        help="Path to jinja2 template. Results will be passed as 'dataset' variable.",
        envvar=common.LACEWORK_REPORTS_TEMPLATE_PATH,
    ),
    tag_column: Optional[typingList[str]] = typer.Option(
        None,
        help="Entity tag keys to use as table column values. This option can be specified multiple times.",
    ),
) -> None:
    """
    Set the command context
    """

    # connect the lacework client
    lw = common.config.connect()

    # report details
    report_title = "Agent Coverage"
    db_table = "discovered_machines"

    reportHelper = ReportHelper()
    db_path = Path("database.db")
    # db_path.unlink(missing_ok=True)
    db_connection = f"sqlite:///{db_path.absolute()}?check_same_thread=False"

    reportHelper.sqlite_drop_table(db_table, db_connection)
    reportHelper.sqlite_drop_table("machines", db_connection)
    reportHelper.sqlite_drop_table("cloud_accounts", db_connection)
    reportHelper.sqlite_drop_table("discovered_machines", db_connection)
    reportHelper.sqlite_drop_table("discovered_cloud_accounts", db_connection)

    has_subaccounts = False
    if subaccounts:
        lwAccounts = reportHelper.get_subaccounts(client=lw)
        if len(lwAccounts) == 0:
            logging.error("Subaccounts specificed but none found")
            raise Exception("Subaccounts specificed but none found")
        else:
            has_subaccounts = True
    else:
        lwAccounts = [{"accountName": lw._account}]

    lacework_account_count = 0
    for lwAccount in lwAccounts:
        lacework_account_count += 1
        if has_subaccounts:
            logging.info(f"Switching to subaccount context: {lwAccount['accountName']}")
            lw.set_subaccount(lwAccount["accountName"])

        # sync cloud accounts with deployed agents
        logging.info("Syncing cloud accounts with deployed agents")
        reportHelper.get_discovered_cloud_accounts(
            client=lw,
            lwAccount=lwAccount["accountName"],
            start_time=start_time,
            end_time=end_time,
            use_sqlite=True,
            db_table="discovered_cloud_accounts",
            db_connection=db_connection,
        )
        try:
            result = reportHelper.sqlite_queries(
                queries={
                    "cloud_account_query": """
                                    SELECT 
                                        DISTINCT ACCOUNTID
                                    FROM 
                                        :db_table
                                    WHERE 
                                        ACCOUNTID IS NOT NULL
                                    """
                },
                db_connection=db_connection,
                db_table="discovered_cloud_accounts",
            )
            discovered_cloud_accounts = [
                x["ACCOUNTID"] for x in result["cloud_account_query"]
            ]
        except Exception:
            discovered_cloud_accounts = []

        # get cloud accounts and sync to sqlite
        cloud_accounts = reportHelper.get_cloud_accounts(
            client=lw, lwAccount=lwAccount["accountName"]
        )
        ExportHandler(
            format=DataHandlerTypes.SQLITE,
            results=[{"data": cloud_accounts}],
            file_path=file_path,
            db_table="cloud_accounts",
            db_connection=db_connection,
        ).export()

        logging.info(
            f"Found {len(cloud_accounts)} cloud accounts from integrations list: {cloud_accounts}"
        )
        logging.info(
            f"Discovered {len(discovered_cloud_accounts)} cloud accounts with agents deployed: {discovered_cloud_accounts}"
        )

        for cloud_account in cloud_accounts:

            if (
                cloud_account["enabled"] == 1
                and cloud_account["accountId"] in discovered_cloud_accounts
            ):
                # sync machines for this cloud account
                logging.info(
                    f"Syncing machines for {lwAccount['accountName']}:{cloud_account['accountId']}"
                )

                # sync all machines with agents
                reportHelper.get_active_machines(
                    client=lw,
                    lwAccount=lwAccount["accountName"],
                    cloud_account=cloud_account["accountId"],
                    start_time=start_time,
                    end_time=end_time,
                    use_sqlite=True,
                    db_table="machines",
                    db_connection=db_connection,
                )

                # sync all discovered ec2 and gce instances
                reportHelper.get_discovered_machines(
                    client=lw,
                    lwAccount=lwAccount["accountName"],
                    cloud_account=cloud_account["accountId"],
                    start_time=start_time,
                    end_time=end_time,
                    use_sqlite=True,
                    db_table="discovered_machines",
                    db_connection=db_connection,
                )

                # ensure we have a machines table
                if not reportHelper.sqlite_table_exists(
                    db_table="machines", db_connection=db_connection
                ):
                    machines_table = """
                                    CREATE TABLE machines (
                                        "LWACCOUNT" TEXT, 
                                        "ACCOUNTID" TEXT, 
                                        "TAG_HOSTNAME" TEXT, 
                                        "TAG_INSTANCEID" TEXT, 
                                        "TAG_ACCOUNTID" TEXT, 
                                        "TAG_PROJECTID" TEXT, 
                                        "TAG_VMPROVIDER" TEXT, 
                                        "LWTOKENSHORT" TEXT
                                    )
                                    """
                    reportHelper.sqlite_execute(
                        query=machines_table, db_connection=db_connection
                    )

                # ensure we have a discovered_machines table
                if not reportHelper.sqlite_table_exists(
                    db_table="discovered_machines", db_connection=db_connection
                ):
                    discovered_machines_table = """
                                                CREATE TABLE discovered_machines (
                                                    "LWACCOUNT" TEXT, 
                                                    "ACCOUNTID" TEXT, 
                                                    "INSTANCEID" TEXT, 
                                                    "NAME" TEXT, 
                                                    "STATE" TEXT, 
                                                    "TAGS" TEXT
                                                )
                                                """
                    reportHelper.sqlite_execute(
                        query=discovered_machines_table, db_connection=db_connection
                    )

            else:
                logging.info(
                    f"Skipping disabled or inactive account {lwAccount['accountName']}:{cloud_account['accountId']}"
                )

    # build custom field extraction
    tag_column_query = ""

    if tag_column is not None:
        tags = tag_column
    else:
        tags = []

    if len(tags) > 0:
        tag_columns = []
        for tag in tags:
            tag_columns.append(
                """
                (SELECT 
                    json_extract(value, '$.Value')
                FROM 
                    json_each( TAGS, '$' ) 
                where
                    json_valid(value) AND json_extract(value, '$.Key') = ':tag'
                LIMIT 1) AS ':tag'
                """.replace(
                    ":tag", tag
                )
            )

        tag_column_query = f"{','.join(tag_columns)},"

    # use sqlite query to generate final result
    results = reportHelper.sqlite_queries(
        queries=AgentQueries,
        db_table=db_table,
        custom_columns=tag_column_query,
        db_connection=db_connection,
    )

    if len(results["report"]) > 0:
        report = results["report"]

        # return additional stats under summary
        stats = {}
        for key in [x for x in results.keys() if x != "report"]:
            stats[key] = results[key]

        # write jinja template
        ExportHandler(
            format=DataHandlerTypes.JINJA2,
            results=[
                {
                    "data": [
                        {
                            "name": db_table,
                            "report": report,
                            "summary": {
                                "rows": len(report),
                                "reportTitle": report_title,
                                "stats": stats,
                            },
                        }
                    ]
                }
            ],
            template_path=template_path,
            file_path=file_path,
        ).export()
    else:
        logging.warn("No results found")


@app.command(name="csv", no_args_is_help=True, help="Generate CSV Report")
def csv_handler(
    ctx: typer.Context,
    start_time: datetime = typer.Option(
        (datetime.utcnow() - timedelta(hours=25)).strftime(common.ISO_FORMAT),
        formats=[common.ISO_FORMAT],
        help="Start time for query period",
    ),
    end_time: datetime = typer.Option(
        (datetime.utcnow()).strftime(common.ISO_FORMAT),
        formats=[common.ISO_FORMAT],
        help="End time for query period",
    ),
    subaccounts: bool = typer.Option(
        False,
        help="Enumerate subaccounts",
        envvar=common.LACEWORK_REPORTS_SUBACCOUNTS,
    ),
    summary_only: bool = typer.Option(
        False,
        help="Return only summary details",
        envvar=common.LACEWORK_REPORTS_SUBACCOUNTS,
    ),
    file_path: str = typer.Option(
        ...,
        help="Path to exported result",
        envvar=common.LACEWORK_REPORTS_FILE_PATH,
    ),
    tag_column: Optional[typingList[str]] = typer.Option(
        None,
        help="Entity tag keys to use as table column values. This option can be specified multiple times.",
    ),
) -> None:
    """
    Set the command context
    """

    # connect the lacework client
    lw = common.config.connect()

    # report details
    # trunk-ignore(flake8/F841)
    report_title = "Agent Coverage"
    db_table = "discovered_machines"

    reportHelper = ReportHelper()
    db_path = Path("database.db")
    # db_path.unlink(missing_ok=True)
    db_connection = f"sqlite:///{db_path.absolute()}?check_same_thread=False"

    reportHelper.sqlite_drop_table(db_table, db_connection)
    reportHelper.sqlite_drop_table("machines", db_connection)
    reportHelper.sqlite_drop_table("cloud_accounts", db_connection)
    reportHelper.sqlite_drop_table("discovered_machines", db_connection)
    reportHelper.sqlite_drop_table("discovered_cloud_accounts", db_connection)

    has_subaccounts = False
    if subaccounts:
        lwAccounts = reportHelper.get_subaccounts(client=lw)
        if len(lwAccounts) == 0:
            logging.error("Subaccounts specificed but none found")
            raise Exception("Subaccounts specificed but none found")
        else:
            has_subaccounts = True
    else:
        lwAccounts = [{"accountName": lw._account}]

    lacework_account_count = 0
    for lwAccount in lwAccounts:
        lacework_account_count += 1
        if has_subaccounts:
            logging.info(f"Switching to subaccount context: {lwAccount['accountName']}")
            lw.set_subaccount(lwAccount["accountName"])

        # sync cloud accounts with deployed agents
        logging.info("Syncing cloud accounts with deployed agents")
        reportHelper.get_discovered_cloud_accounts(
            client=lw,
            lwAccount=lwAccount["accountName"],
            start_time=start_time,
            end_time=end_time,
            use_sqlite=True,
            db_table="discovered_cloud_accounts",
            db_connection=db_connection,
        )
        try:
            result = reportHelper.sqlite_queries(
                queries={
                    "cloud_account_query": """
                                    SELECT 
                                        DISTINCT ACCOUNTID
                                    FROM 
                                        :db_table
                                    WHERE 
                                        ACCOUNTID IS NOT NULL
                                    """
                },
                db_connection=db_connection,
                db_table="discovered_cloud_accounts",
            )
            discovered_cloud_accounts = [
                x["ACCOUNTID"] for x in result["cloud_account_query"]
            ]
        except Exception:
            discovered_cloud_accounts = []

        # get cloud accounts and sync to sqlite
        cloud_accounts = reportHelper.get_cloud_accounts(
            client=lw, lwAccount=lwAccount["accountName"]
        )
        ExportHandler(
            format=DataHandlerTypes.SQLITE,
            results=[{"data": cloud_accounts}],
            file_path=file_path,
            db_table="cloud_accounts",
            db_connection=db_connection,
        ).export()

        logging.info(
            f"Discovered {len(discovered_cloud_accounts)} cloud accounts with agents deployed: {discovered_cloud_accounts}"
        )

        for cloud_account in cloud_accounts:

            if (
                cloud_account["enabled"] == 1
                and cloud_account["accountId"] in discovered_cloud_accounts
            ):
                # sync machines for this cloud account
                logging.info(
                    f"Syncing machines for {lwAccount['accountName']}:{cloud_account['accountId']}"
                )

                # sync all machines with agents
                reportHelper.get_active_machines(
                    client=lw,
                    lwAccount=lwAccount["accountName"],
                    cloud_account=cloud_account["accountId"],
                    start_time=start_time,
                    end_time=end_time,
                    use_sqlite=True,
                    db_table="machines",
                    db_connection=db_connection,
                )

                # sync all discovered ec2 and gce instances
                reportHelper.get_discovered_machines(
                    client=lw,
                    lwAccount=lwAccount["accountName"],
                    cloud_account=cloud_account["accountId"],
                    start_time=start_time,
                    end_time=end_time,
                    use_sqlite=True,
                    db_table="discovered_machines",
                    db_connection=db_connection,
                )

                # ensure we have a machines table
                if not reportHelper.sqlite_table_exists(
                    db_table="machines", db_connection=db_connection
                ):
                    machines_table = """
                                    CREATE TABLE machines (
                                        "LWACCOUNT" TEXT, 
                                        "ACCOUNTID" TEXT, 
                                        "TAG_HOSTNAME" TEXT, 
                                        "TAG_INSTANCEID" TEXT, 
                                        "TAG_ACCOUNTID" TEXT, 
                                        "TAG_PROJECTID" TEXT, 
                                        "TAG_VMPROVIDER" TEXT, 
                                        "LWTOKENSHORT" TEXT
                                    )
                                    """
                    reportHelper.sqlite_execute(
                        query=machines_table, db_connection=db_connection
                    )

                # ensure we have a discovered_machines table
                if not reportHelper.sqlite_table_exists(
                    db_table="discovered_machines", db_connection=db_connection
                ):
                    discovered_machines_table = """
                                                CREATE TABLE discovered_machines (
                                                    "LWACCOUNT" TEXT, 
                                                    "ACCOUNTID" TEXT, 
                                                    "INSTANCEID" TEXT, 
                                                    "NAME" TEXT, 
                                                    "STATE" TEXT, 
                                                    "TAGS" TEXT
                                                )
                                                """
                    reportHelper.sqlite_execute(
                        query=discovered_machines_table, db_connection=db_connection
                    )

            else:
                logging.info(
                    f"Skipping disabled or inactive account {lwAccount['accountName']}:{cloud_account['accountId']}"
                )

    # build custom field extraction
    tag_column_query = ""

    if tag_column is not None:
        tags = tag_column
    else:
        tags = []

    if len(tags) > 0:
        tag_columns = []
        for tag in tags:
            tag_columns.append(
                """
                (SELECT 
                    json_extract(value, '$.Value')
                FROM 
                    json_each( TAGS, '$' ) 
                where
                    json_valid(value) AND json_extract(value, '$.Key') = ':tag'
                LIMIT 1) AS ':tag'
                """.replace(
                    ":tag", tag
                )
            )

        tag_column_query = f"{','.join(tag_columns)},"

    # use sqlite query to generate final result
    results = reportHelper.sqlite_queries(
        queries=AgentQueries,
        db_table=db_table,
        custom_columns=tag_column_query,
        db_connection=db_connection,
    )

    if len(results["report"]) > 0:
        report = results["report"]
        if summary_only:
            report = results["account_coverage"]

        logging.info("Building CSV from resultant data...")
        ExportHandler(
            format=DataHandlerTypes.CSV,
            results=[{"data": report}],
            file_path=file_path,
        ).export()
    else:
        logging.warn("No results found")


if __name__ == "__main__":
    app()
