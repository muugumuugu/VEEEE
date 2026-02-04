"""Admin and creator routes for VoiceExpress."""
from __future__ import annotations

from datetime import date

from flask import Blueprint, redirect, render_template, request, session, url_for

from .data import ARTIFACTS, CATEGORIES, TAGS, USERS, Artifact, Citation

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _is_editor() -> bool:
    user_name = session.get("user")
    return bool(user_name and USERS.get(user_name) and USERS[user_name].role in {"Editor", "Admin"})


@admin_bp.route("/")
def dashboard() -> str:
    """Render the editorial dashboard with creator modes."""
    return render_template("admin/dashboard.html", is_editor=_is_editor())


@admin_bp.route("/create", methods=["GET", "POST"])
def create_artifact() -> str:
    """Create a new artifact with full metadata and citations."""
    if not _is_editor():
        return redirect(url_for("auth.login"))

    message = ""
    if request.method == "POST":
        next_id = max(artifact.id for artifact in ARTIFACTS) + 1
        citations = [
            Citation(
                label=request.form.get("citation_label", "").strip() or "Field Note",
                source=request.form.get("citation_source", "").strip() or "VoiceExpress Archive",
                url=request.form.get("citation_url", "").strip() or "https://example.com",
            )
        ]
        artifact = Artifact(
            id=next_id,
            title=request.form.get("title", "Untitled").strip(),
            tagline=request.form.get("tagline", ""),
            synopsis=request.form.get("synopsis", ""),
            byline=f"By {request.form.get('byline', 'Staff Writer')}",
            author_note=request.form.get("author_note", ""),
            editor_note=request.form.get("editor_note", ""),
            body=request.form.get("body", ""),
            category=request.form.get("category", CATEGORIES[0]),
            tags=[tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()],
            location=request.form.get("location", ""),
            published=date.today(),
            citations=citations,
            artifact_type=request.form.get("artifact_type", "article"),
            image="/static/images/placeholder.jpg",
            issue=request.form.get("issue", "June 2024"),
            geotag=request.form.get("geotag", "0.0000,0.0000"),
            abstract_tag=request.form.get("abstract_tag", "Unnamed Orbit"),
        )
        ARTIFACTS.append(artifact)
        message = "Artifact created and routed to editorial review."

    return render_template(
        "admin/create.html",
        categories=CATEGORIES,
        tags=TAGS,
        message=message,
    )


@admin_bp.route("/tags", methods=["GET", "POST"])
def manage_tags() -> str:
    """Create tags used across artifacts."""
    if not _is_editor():
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        tag = request.form.get("tag", "").strip()
        if tag and tag not in TAGS:
            TAGS.append(tag)
    return render_template("admin/tags.html", tags=TAGS)


@admin_bp.route("/categories", methods=["GET", "POST"])
def manage_categories() -> str:
    """Create categories used across artifacts."""
    if not _is_editor():
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        if category and category not in CATEGORIES:
            CATEGORIES.append(category)
    return render_template("admin/categories.html", categories=CATEGORIES)
