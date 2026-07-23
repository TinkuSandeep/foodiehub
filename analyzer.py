from __future__ import annotations

import io
import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
from rapidfuzz import fuzz


# ---------------------------------------------------------------------------
# Column aliases
# ---------------------------------------------------------------------------

INCIDENT_ALIASES: dict[str, list[str]] = {
    "number": [
        "number", "incident", "incident number", "ticket", "ticket number",
        "task number", "inc number",
    ],
    "short_description": [
        "short description", "short_description", "summary", "title",
        "brief description",
    ],
    "description": [
        "description", "details", "work notes", "work_notes", "comments",
        "additional comments", "close notes", "close_notes", "resolution notes",
    ],
    "opened_at": [
        "opened", "opened at", "opened_at", "created", "created at",
        "created_on", "sys created on", "sys_created_on",
    ],
    "closed_at": [
        "closed", "closed at", "closed_at", "resolved", "resolved at",
        "resolved_at", "completed", "completed at",
    ],
    "assignment_group": [
        "assignment group", "assignment_group", "support group", "group",
        "assigned group",
    ],
    "application": [
        "application", "business application", "business service",
        "configuration item", "configuration_item", "config item", "ci",
        "service", "application name", "app name",
    ],
    "state": ["state", "status", "incident state"],
    "priority": ["priority", "severity", "impact"],
    "category": ["category", "subcategory", "sub category"],
}

CHANGE_ALIASES: dict[str, list[str]] = {
    "number": [
        "number", "change", "change number", "change request", "standard change",
        "ticket", "task number", "chg number",
    ],
    "short_description": [
        "short description", "short_description", "summary", "title",
        "brief description",
    ],
    "description": [
        "description", "details", "work notes", "work_notes", "comments",
        "close notes", "close_notes", "implementation plan",
        "implementation_plan", "justification", "backout plan",
    ],
    "opened_at": [
        "opened", "opened at", "opened_at", "created", "created at",
        "created_on", "sys created on", "sys_created_on", "planned start",
        "planned start date",
    ],
    "closed_at": [
        "closed", "closed at", "closed_at", "completed", "completed at",
        "completed_at", "planned end", "planned end date",
    ],
    "assignment_group": [
        "assignment group", "assignment_group", "support group", "group",
        "assigned group",
    ],
    "application": [
        "application", "business application", "business service",
        "configuration item", "configuration_item", "config item", "ci",
        "service", "application name", "app name",
    ],
    "state": ["state", "status", "change state"],
    "priority": ["priority", "risk", "impact"],
    "category": ["category", "type", "change type", "model"],
}


# ---------------------------------------------------------------------------
# Classification dictionaries
# ---------------------------------------------------------------------------

UPSTREAM_MISSING_TERMS = [
    "upstream", "source team", "source system", "source file",
    "file not received", "file not available", "file unavailable",
    "file missing", "missing file", "waiting for file", "awaiting file",
    "late file", "file delayed", "file delay", "delayed file",
    "input file", "inbound file", "file arrival", "landing path",
    "landing folder", "nas path", "sftp path", "ftp path",
]

DATA_QUALITY_TERMS = [
    "corrupt file", "corrupted file", "file corrupt", "bad data",
    "invalid data", "invalid record", "malformed", "extra character",
    "special character", "delimiter issue", "incorrect delimiter",
    "column mismatch", "missing column", "additional column",
    "unexpected column", "header mismatch", "invalid header",
    "trailer mismatch", "record length", "field length", "value too long",
    "truncation", "data type mismatch", "conversion failed",
    "invalid date", "null value", "duplicate record", "duplicate row",
    "schema mismatch", "format issue", "invalid format", "encoding issue",
    "file structure", "data quality",
]

TRANSFER_TERMS = [
    "sftp", "ftp", "file transfer", "transfer failed", "connection refused",
    "connection timeout", "network issue", "network failure", "permission denied",
    "access denied", "authentication failed", "credentials", "ssh",
    "path not found", "directory not found", "nas unavailable",
]

DATABASE_TERMS = [
    "database", "sql", "oracle", "postgres", "db2", "deadlock",
    "constraint violation", "primary key", "foreign key", "insert failed",
    "table", "stored procedure", "connection pool", "database unavailable",
]

AUTOSYS_TERMS = [
    "autosys", "autorep", "jil", "box job", "job status", "force start",
]

SSIS_TERMS = [
    "ssis", "sql server integration services", "dtsx", "package execution",
]

JOB_FAILURE_TERMS = [
    "job failed", "job failure", "batch failed", "package failed",
    "execution failed", "abend", "terminated", "not running", "failed job",
    "restart job", "rerun", "re-run", "force start", "force-start",
]

RECOVERY_TERMS = [
    "file available", "file is available", "file received", "file arrived",
    "restart", "rerun", "re-run", "force start", "force-start",
    "completed successfully", "job success", "job completed",
    "validated successfully", "processing completed",
]


@dataclass
class AnalysisResult:
    run_id: str
    incidents: pd.DataFrame
    changes: pd.DataFrame
    correlated: pd.DataFrame
    summary: dict[str, Any]
    output_dir: Path


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _norm(value: Any) -> str:
    """Normalize text safely for comparison."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"[_/\\\-]+", " ", text)
    return re.sub(r"\s+", " ", text)


def _safe_text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    normalized = _norm(text)
    return any(term in normalized for term in terms)


def _find_column(columns: list[str], aliases: list[str]) -> str | None:
    """Find the best matching source column for a canonical field."""
    normalized = {_norm(column): column for column in columns}

    # Exact normalized match first.
    for alias in aliases:
        match = normalized.get(_norm(alias))
        if match:
            return match

    # Token/substring match second.
    best_column: str | None = None
    best_score = 0
    for alias in aliases:
        alias_norm = _norm(alias)
        for normalized_name, original_name in normalized.items():
            if alias_norm in normalized_name or normalized_name in alias_norm:
                score = min(len(alias_norm), len(normalized_name))
                if score > best_score:
                    best_score = score
                    best_column = original_name

    return best_column


def _empty_series(length: int, dtype: str = "object") -> pd.Series:
    return pd.Series([""] * length, dtype=dtype)


def _ensure_columns(frame: pd.DataFrame, defaults: dict[str, Any]) -> pd.DataFrame:
    """Guarantee required columns exist and prevent KeyError failures."""
    result = frame.copy()
    for column, default in defaults.items():
        if column not in result.columns:
            result[column] = default
    return result


def _parse_datetime(series: pd.Series) -> pd.Series:
    """Parse ServiceNow timestamps while tolerating mixed formats."""
    return pd.to_datetime(series, errors="coerce", format="mixed")


def _clean_application(value: Any) -> str:
    text = _safe_text(value)
    if not text:
        return "Unknown"

    # ServiceNow exports sometimes include display values such as:
    # "Application Name [CI12345]" or "Application Name | Environment".
    text = re.sub(r"\s*\[[^\]]+\]\s*$", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or "Unknown"


# ---------------------------------------------------------------------------
# Excel ingestion and normalization
# ---------------------------------------------------------------------------

def read_excel_bytes(content: bytes) -> pd.DataFrame:
    """
    Read the first usable sheet from an Excel workbook.

    Empty title sheets and introductory sheets are skipped automatically.
    """
    if not content:
        raise ValueError("The uploaded Excel file is empty.")

    workbook = pd.ExcelFile(io.BytesIO(content))
    if not workbook.sheet_names:
        raise ValueError("The uploaded workbook does not contain any worksheets.")

    candidates: list[pd.DataFrame] = []
    for sheet_name in workbook.sheet_names:
        frame = pd.read_excel(workbook, sheet_name=sheet_name)
        frame = frame.dropna(how="all").dropna(axis=1, how="all")
        if not frame.empty:
            candidates.append(frame)

    if not candidates:
        raise ValueError("No data rows were found in the uploaded workbook.")

    # Prefer the sheet with the greatest number of populated cells.
    return max(
        candidates,
        key=lambda frame: int(frame.notna().sum().sum()),
    )


def normalize_frame(df: pd.DataFrame, kind: str) -> pd.DataFrame:
    """
    Convert varying ServiceNow exports into a stable internal schema.

    Missing source fields are represented by blank/default values rather than
    causing analysis failures.
    """
    if kind not in {"incident", "change"}:
        raise ValueError("kind must be either 'incident' or 'change'.")

    source = df.copy()
    source.columns = [str(column).strip() for column in source.columns]
    source = source.dropna(how="all").reset_index(drop=True)

    aliases = INCIDENT_ALIASES if kind == "incident" else CHANGE_ALIASES
    out = pd.DataFrame(index=source.index)

    for canonical, candidates in aliases.items():
        source_column = _find_column(list(source.columns), candidates)
        if source_column is None:
            out[canonical] = _empty_series(len(source))
        else:
            out[canonical] = source[source_column]

    text_fields = [
        "number", "short_description", "description", "assignment_group",
        "application", "state", "priority", "category",
    ]
    for field in text_fields:
        out[field] = out[field].fillna("").astype(str).str.strip()

    out["opened_at"] = _parse_datetime(out["opened_at"])
    out["closed_at"] = _parse_datetime(out["closed_at"])

    # Use a synthetic record number when the export omits a number column.
    missing_number = out["number"].eq("")
    prefix = "INC" if kind == "incident" else "CHG"
    synthetic_numbers = [
        f"{prefix}-ROW-{index + 2}" for index in range(len(out))
    ]
    out.loc[missing_number, "number"] = pd.Series(
        synthetic_numbers, index=out.index
    )[missing_number]

    out["record_type"] = kind
    out["application_normalized"] = out["application"].apply(_clean_application)

    out["text"] = (
        out["short_description"].fillna("") + " " +
        out["description"].fillna("") + " " +
        out["application"].fillna("") + " " +
        out["category"].fillna("")
    ).str.lower().str.replace(r"\s+", " ", regex=True).str.strip()

    out["job_platform"] = out["text"].apply(classify_platform)
    out["root_cause_category"] = out["text"].apply(classify_root_cause)
    out["is_upstream_file_failure"] = out.apply(
        lambda row: classify_upstream(
            row["text"],
            record_type=kind,
            root_cause=row["root_cause_category"],
        ),
        axis=1,
    )

    duration = (
        out["closed_at"] - out["opened_at"]
    ).dt.total_seconds().div(3600)

    # Negative durations indicate inconsistent source dates and are ignored.
    out["duration_hours"] = duration.where(duration >= 0).round(2)

    return _ensure_columns(
        out,
        {
            "number": "",
            "short_description": "",
            "description": "",
            "opened_at": pd.NaT,
            "closed_at": pd.NaT,
            "assignment_group": "",
            "application": "",
            "application_normalized": "Unknown",
            "state": "",
            "priority": "",
            "category": "",
            "record_type": kind,
            "text": "",
            "is_upstream_file_failure": False,
            "job_platform": "Unknown",
            "root_cause_category": "Other / Unclassified",
            "duration_hours": pd.NA,
        },
    )


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_platform(text: str) -> str:
    normalized = _norm(text)
    has_autosys = any(term in normalized for term in AUTOSYS_TERMS)
    has_ssis = any(term in normalized for term in SSIS_TERMS)

    if has_autosys and has_ssis:
        return "AutoSys + SSIS"
    if has_autosys:
        return "AutoSys"
    if has_ssis:
        return "SSIS"
    if "batch" in normalized or "job" in normalized or "package" in normalized:
        return "Other Batch"
    return "Unknown"


def classify_root_cause(text: str) -> str:
    normalized = _norm(text)

    if _contains_any(normalized, DATA_QUALITY_TERMS):
        return "File Data Quality / Format"
    if _contains_any(normalized, TRANSFER_TERMS):
        return "File Transfer / Connectivity"
    if _contains_any(normalized, UPSTREAM_MISSING_TERMS):
        return "Upstream File Missing / Delayed"
    if _contains_any(normalized, DATABASE_TERMS):
        return "Database / Load Failure"
    if _contains_any(normalized, AUTOSYS_TERMS + SSIS_TERMS + JOB_FAILURE_TERMS):
        return "Job / Scheduler Failure"
    return "Other / Unclassified"


def classify_upstream(
    text: str,
    *,
    record_type: str = "incident",
    root_cause: str | None = None,
) -> bool:
    """
    Identify records connected to upstream-file operational failures.

    Incidents normally require both a file/dependency signal and a job/load
    failure signal. Changes are allowed to qualify through recovery wording,
    because standard changes often contain only restart instructions.
    """
    normalized = _norm(text)
    cause = root_cause or classify_root_cause(normalized)

    file_signal = (
        _contains_any(normalized, UPSTREAM_MISSING_TERMS)
        or _contains_any(normalized, DATA_QUALITY_TERMS)
        or _contains_any(normalized, TRANSFER_TERMS)
    )
    processing_signal = (
        _contains_any(normalized, JOB_FAILURE_TERMS)
        or _contains_any(normalized, AUTOSYS_TERMS)
        or _contains_any(normalized, SSIS_TERMS)
        or _contains_any(normalized, DATABASE_TERMS)
        or "load failed" in normalized
        or "processing failed" in normalized
    )
    recovery_signal = _contains_any(normalized, RECOVERY_TERMS)

    if record_type == "change":
        return (file_signal and (processing_signal or recovery_signal)) or (
            recovery_signal
            and _contains_any(normalized, AUTOSYS_TERMS + SSIS_TERMS)
        )

    if cause in {
        "File Data Quality / Format",
        "File Transfer / Connectivity",
        "Upstream File Missing / Delayed",
    }:
        return file_signal and processing_signal

    return file_signal and processing_signal


# ---------------------------------------------------------------------------
# Correlation
# ---------------------------------------------------------------------------

def _hours_between(left: Any, right: Any) -> float | None:
    if pd.isna(left) or pd.isna(right):
        return None
    try:
        return abs((right - left).total_seconds()) / 3600
    except (AttributeError, TypeError, ValueError):
        return None


def _correlation_score(incident: pd.Series, change: pd.Series) -> float:
    incident_text = _norm(
        f"{incident.get('short_description', '')} "
        f"{incident.get('description', '')} "
        f"{incident.get('application_normalized', '')}"
    )
    change_text = _norm(
        f"{change.get('short_description', '')} "
        f"{change.get('description', '')} "
        f"{change.get('application_normalized', '')}"
    )

    score = float(fuzz.token_set_ratio(incident_text, change_text))

    incident_app = _norm(incident.get("application_normalized", ""))
    change_app = _norm(change.get("application_normalized", ""))
    if (
        incident_app
        and change_app
        and incident_app != "unknown"
        and incident_app == change_app
    ):
        score += 22

    incident_platform = _safe_text(incident.get("job_platform", "Unknown"))
    change_platform = _safe_text(change.get("job_platform", "Unknown"))
    if (
        incident_platform != "Unknown"
        and incident_platform == change_platform
    ):
        score += 10

    incident_cause = _safe_text(
        incident.get("root_cause_category", "Other / Unclassified")
    )
    change_cause = _safe_text(
        change.get("root_cause_category", "Other / Unclassified")
    )
    if (
        incident_cause != "Other / Unclassified"
        and incident_cause == change_cause
    ):
        score += 8

    hours = _hours_between(
        incident.get("opened_at", pd.NaT),
        change.get("opened_at", pd.NaT),
    )
    if hours is not None:
        if hours <= 24:
            score += 18
        elif hours <= 72:
            score += 12
        elif hours <= 168:
            score += 5
        elif hours > 336:
            score -= 20

    return score


def correlate(
    incidents: pd.DataFrame,
    changes: pd.DataFrame,
    minimum_score: float = 48.0,
) -> pd.DataFrame:
    """Correlate upstream incidents to the most likely standard change."""
    incident_defaults = {
        "is_upstream_file_failure": False,
        "number": "",
        "opened_at": pd.NaT,
        "closed_at": pd.NaT,
        "application_normalized": "Unknown",
        "job_platform": "Unknown",
        "root_cause_category": "Other / Unclassified",
        "short_description": "",
        "description": "",
        "duration_hours": pd.NA,
    }
    change_defaults = {
        "number": "",
        "opened_at": pd.NaT,
        "state": "",
        "application_normalized": "Unknown",
        "job_platform": "Unknown",
        "root_cause_category": "Other / Unclassified",
        "short_description": "",
        "description": "",
    }

    safe_incidents = _ensure_columns(incidents, incident_defaults)
    safe_changes = _ensure_columns(changes, change_defaults)
    upstream_incidents = safe_incidents[
        safe_incidents["is_upstream_file_failure"].fillna(False).astype(bool)
    ].copy()

    output_columns = [
        "incident_number", "incident_opened_at", "incident_closed_at",
        "application", "job_platform", "root_cause_category",
        "incident_summary", "change_number", "change_opened_at",
        "change_state", "correlation_score", "matched",
        "manual_recovery_detected", "resolution_hours",
    ]

    if upstream_incidents.empty:
        return pd.DataFrame(columns=output_columns)

    rows: list[dict[str, Any]] = []

    for _, incident in upstream_incidents.iterrows():
        best_score = 0.0
        best_change: pd.Series | None = None

        for _, change in safe_changes.iterrows():
            score = _correlation_score(incident, change)
            if score > best_score:
                best_score = score
                best_change = change

        matched = best_change is not None and best_score >= minimum_score
        incident_text = _norm(
            f"{incident.get('short_description', '')} "
            f"{incident.get('description', '')}"
        )

        rows.append(
            {
                "incident_number": _safe_text(incident.get("number", "")),
                "incident_opened_at": incident.get("opened_at", pd.NaT),
                "incident_closed_at": incident.get("closed_at", pd.NaT),
                "application": _safe_text(
                    incident.get("application_normalized", "Unknown")
                ) or "Unknown",
                "job_platform": _safe_text(
                    incident.get("job_platform", "Unknown")
                ) or "Unknown",
                "root_cause_category": _safe_text(
                    incident.get(
                        "root_cause_category",
                        "Other / Unclassified",
                    )
                ),
                "incident_summary": _safe_text(
                    incident.get("short_description", "")
                ),
                "change_number": (
                    _safe_text(best_change.get("number", ""))
                    if matched and best_change is not None
                    else ""
                ),
                "change_opened_at": (
                    best_change.get("opened_at", pd.NaT)
                    if matched and best_change is not None
                    else pd.NaT
                ),
                "change_state": (
                    _safe_text(best_change.get("state", ""))
                    if matched and best_change is not None
                    else ""
                ),
                "correlation_score": round(best_score, 1) if matched else 0.0,
                "matched": bool(matched),
                "manual_recovery_detected": bool(
                    _contains_any(incident_text, RECOVERY_TERMS) or matched
                ),
                "resolution_hours": pd.to_numeric(
                    incident.get("duration_hours", pd.NA),
                    errors="coerce",
                ),
            }
        )

    return pd.DataFrame(rows, columns=output_columns)


# ---------------------------------------------------------------------------
# Summary and orchestration
# ---------------------------------------------------------------------------

def build_summary(
    incidents: pd.DataFrame,
    changes: pd.DataFrame,
    correlated: pd.DataFrame,
) -> dict[str, Any]:
    safe_incidents = _ensure_columns(
        incidents,
        {
            "is_upstream_file_failure": False,
            "duration_hours": pd.NA,
            "application_normalized": "Unknown",
            "job_platform": "Unknown",
            "root_cause_category": "Other / Unclassified",
            "opened_at": pd.NaT,
        },
    )
    safe_correlated = _ensure_columns(
        correlated,
        {"matched": False},
    )

    upstream_incidents = safe_incidents[
        safe_incidents["is_upstream_file_failure"].fillna(False).astype(bool)
    ].copy()

    matched = safe_correlated[
        safe_correlated["matched"].fillna(False).astype(bool)
    ].copy()

    hours = pd.to_numeric(
        upstream_incidents["duration_hours"],
        errors="coerce",
    )
    valid_hours = hours[(hours >= 0) & hours.notna()]

    estimated_minutes = int(
        len(upstream_incidents) * 75
        + len(matched) * 30
    )

    application_counts = (
        upstream_incidents["application_normalized"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .head(10)
        .to_dict()
    )
    platform_counts = (
        upstream_incidents["job_platform"]
        .fillna("Unknown")
        .replace("", "Unknown")
        .value_counts()
        .to_dict()
    )
    root_cause_counts = (
        upstream_incidents["root_cause_category"]
        .fillna("Other / Unclassified")
        .replace("", "Other / Unclassified")
        .value_counts()
        .to_dict()
    )

    monthly: dict[str, int] = {}
    opened = upstream_incidents.dropna(subset=["opened_at"]).copy()
    if not opened.empty:
        opened["month"] = opened["opened_at"].dt.strftime("%Y-%m")
        monthly = (
            opened["month"]
            .value_counts()
            .sort_index()
            .astype(int)
            .to_dict()
        )

    upstream_count = len(upstream_incidents)
    matched_count = len(matched)

    return {
        "total_incidents_uploaded": int(len(safe_incidents)),
        "total_changes_uploaded": int(len(changes)),
        "upstream_file_incidents": int(upstream_count),
        "correlated_standard_changes": int(matched_count),
        "unmatched_upstream_incidents": int(
            max(len(safe_correlated) - matched_count, 0)
        ),
        "average_resolution_hours": (
            round(float(valid_hours.mean()), 2)
            if not valid_hours.empty
            else 0
        ),
        "median_resolution_hours": (
            round(float(valid_hours.median()), 2)
            if not valid_hours.empty
            else 0
        ),
        "estimated_manual_effort_hours": round(
            estimated_minutes / 60,
            1,
        ),
        "top_applications": application_counts,
        "platform_distribution": platform_counts,
        "root_cause_distribution": root_cause_counts,
        "monthly_trend": monthly,
        "automation_opportunity_pct": (
            round(matched_count / upstream_count * 100, 1)
            if upstream_count
            else 0
        ),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def analyze(
    incident_bytes: bytes,
    change_bytes: bytes,
    base_output: Path,
) -> AnalysisResult:
    """Run the full analysis and persist normalized CSV outputs."""
    run_id = uuid.uuid4().hex[:10]
    output_dir = base_output / run_id
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_incidents = read_excel_bytes(incident_bytes)
    raw_changes = read_excel_bytes(change_bytes)

    incidents = normalize_frame(raw_incidents, "incident")
    changes = normalize_frame(raw_changes, "change")
    correlated = correlate(incidents, changes)
    summary = build_summary(incidents, changes, correlated)

    incidents.to_csv(
        output_dir / "normalized_incidents.csv",
        index=False,
        encoding="utf-8-sig",
    )
    changes.to_csv(
        output_dir / "normalized_changes.csv",
        index=False,
        encoding="utf-8-sig",
    )
    correlated.to_csv(
        output_dir / "correlated_cases.csv",
        index=False,
        encoding="utf-8-sig",
    )

    return AnalysisResult(
        run_id=run_id,
        incidents=incidents,
        changes=changes,
        correlated=correlated,
        summary=summary,
        output_dir=output_dir,
    )
