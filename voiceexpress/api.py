"""API endpoints for export and structured feeds."""
from __future__ import annotations

import json
from typing import Dict

from flask import Blueprint, Response

from .data import ARTIFACTS, find_artifact

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _artifact_payload(artifact) -> Dict[str, object]:
    return {
        "id": artifact.id,
        "title": artifact.title,
        "tagline": artifact.tagline,
        "synopsis": artifact.synopsis,
        "byline": artifact.byline,
        "author_note": artifact.author_note,
        "editor_note": artifact.editor_note,
        "body": artifact.body,
        "category": artifact.category,
        "tags": artifact.tags,
        "location": artifact.location,
        "published": artifact.published.isoformat(),
        "citations": [citation.__dict__ for citation in artifact.citations],
        "artifact_type": artifact.artifact_type,
        "issue": artifact.issue,
        "geotag": artifact.geotag,
        "abstract_tag": artifact.abstract_tag,
    }


@api_bp.route("/artifacts")
def artifacts_feed() -> Response:
    """Return a JSON feed for all artifacts."""
    payload = [_artifact_payload(artifact) for artifact in ARTIFACTS]
    return Response(json.dumps(payload, indent=2), mimetype="application/json")


@api_bp.route("/export/<int:artifact_id>.<format>")
def export_artifact(artifact_id: int, format: str) -> Response:
    """Export artifacts as JSON, XML, or Markdown."""
    artifact = find_artifact(artifact_id)
    if not artifact:
        return Response("Not found", status=404)
    if format == "json":
        return Response(
            json.dumps(_artifact_payload(artifact), indent=2),
            mimetype="application/json",
        )
    if format == "md":
        markdown = (
            f"# {artifact.title}\n\n"
            f"*{artifact.tagline}*\n\n"
            f"{artifact.byline} | {artifact.location} | {artifact.published.isoformat()}\n\n"
            f"## Synopsis\n{artifact.synopsis}\n\n"
            f"## Body\n{artifact.body}\n\n"
            f"## Notes\nAuthor: {artifact.author_note}\nEditor: {artifact.editor_note}\n"
        )
        return Response(markdown, mimetype="text/markdown")
    if format == "xml":
        citations_xml = "".join(
            f"<citation label=\"{citation.label}\" source=\"{citation.source}\" url=\"{citation.url}\" />"
            for citation in artifact.citations
        )
        xml = (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            f"<artifact id=\"{artifact.id}\">"
            f"<title>{artifact.title}</title>"
            f"<tagline>{artifact.tagline}</tagline>"
            f"<synopsis>{artifact.synopsis}</synopsis>"
            f"<byline>{artifact.byline}</byline>"
            f"<body>{artifact.body}</body>"
            f"<citations>{citations_xml}</citations>"
            "</artifact>"
        )
        return Response(xml, mimetype="application/xml")
    return Response("Unsupported format", status=400)
