import os
import agilicus
from agilicus import ApiException

import json
from .input_helpers import get_org_from_input_or_ctx
from .output import output_if_console
from .context import get_apiclient_from_ctx
import operator

from .output.table import (
    column,
    spec_column,
    status_column,
    metadata_column,
    format_table,
    subtable,
)


def get_billing_account(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.get_billing_account(billing_account_id, **kwargs)


def list_accounts(ctx, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.list_billing_accounts(**kwargs)


def format_accounts(ctx, accounts):
    orgs_column = [column("id"), column("organisation")]
    products_column = [
        column("name"),
    ]
    columns = [
        metadata_column("id"),
        spec_column("customer_id"),
        spec_column("dev_mode"),
        status_column("customer", optional=True),
        subtable(ctx, "products", products_column, subobject_name="status"),
        subtable(ctx, "orgs", orgs_column, subobject_name="status"),
    ]
    return format_table(ctx, accounts, columns)


def add_billing_account(ctx, customer_id=None, dev_mode=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    spec = agilicus.BillingAccountSpec(customer_id=customer_id)

    if dev_mode is not None:
        spec.dev_mode = dev_mode

    account = agilicus.BillingAccount(spec=spec)

    return client.billing_api.create_billing_account(account)


def add_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    billing_org = agilicus.BillingOrg._from_openapi_data(org_id=org_id)
    return client.billing_api.add_org_to_billing_account(
        billing_account_id, billing_org=billing_org
    )


def remove_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.remove_org_from_billing_account(billing_account_id, org_id)


def replace_billing_account(
    ctx, billing_account_id=None, customer_id=None, dev_mode=None, **kwargs
):
    client = get_apiclient_from_ctx(ctx)

    existing = client.billing_api.get_billing_account(billing_account_id)
    if customer_id is not None:
        existing.spec.customer_id = customer_id
    if dev_mode is not None:
        existing.spec.dev_mode = dev_mode
    return client.billing_api.replace_billing_account(
        billing_account_id, billing_account=existing
    )


def format_usage_records(ctx, records):
    columns = [
        column("id"),
        column("period"),
        column("total_usage"),
    ]
    return format_table(ctx, records, columns, getter=operator.itemgetter)


def get_usage_records(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_usage_records(billing_account_id)


def run_billing_um_all_accounts(
    ctx, client, dry_run=False, push_to_prometheus_on_success=True, **kwargs
):
    accounts = client.billing_api.list_billing_accounts()
    record = agilicus.CreateBillingUsageRecords(dry_run=dry_run)
    numSuccess = 0
    numFail = 0
    for account in accounts.billing_accounts:
        if not account.spec.customer_id:
            continue
        try:
            result = client.billing_api.add_billing_usage_record(
                account.metadata.id, create_billing_usage_records=record
            ).to_dict()

            result["billing_account"] = account.metadata.id
            result["customer_id"] = account.spec.customer_id
            result["orgs"] = [
                {"id": org.id, "organisation": org.organisation}
                for org in account.status.orgs
            ]
            numSuccess += 1
            print(json.dumps(result))
        except ApiException as exc:
            numFail += 1
            print(exc.body)
        except Exception as exc:
            numFail += 1
            print(str(exc))

    if push_to_prometheus_on_success:
        try:
            from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
        except ModuleNotFoundError:
            output_if_console(ctx, "Not posting success to prometheus_client.")
            output_if_console(
                ctx, "Add the 'billing' option to the install to gain access"
            )
            return

        registry = CollectorRegistry()
        gSuccess = Gauge(
            "billing_usage_records_created_count",
            "number of billing accounts that have created a usage record",
            registry=registry,
        )

        gFail = Gauge(
            "billing_usage_records_failed_count",
            "number of billing accounts that failed to create a usage record",
            registry=registry,
        )

        push_gateway = os.environ.get(
            "PROMETHEUS_PUSH_GATEWAY",
            "push-prometheus-pushgateway.prometheus-pushgateway:9091",
        )
        job_name = os.environ.get("JOB_NAME", "billing_usage_job")
        gSuccess.set(numSuccess)
        gFail.set(numFail)
        push_to_gateway(push_gateway, job=job_name, registry=registry)


def create_usage_record(
    ctx, billing_account_id=None, all_accounts=None, dry_run=False, **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    record = agilicus.BillingUsageRecord(dry_run=dry_run)
    if billing_account_id is not None:
        result = client.billing_api.add_billing_usage_record(
            billing_account_id, billing_usage_record=record
        )
        print(json.dumps(result.to_dict()))
    elif all_accounts is not None:
        run_billing_um_all_accounts(ctx, client, dry_run=dry_run, **kwargs)
    else:
        raise Exception("Need to choose --billing-account-or or --all-accounts")
