"""Public-facing routes for VoiceExpress."""
from __future__ import annotations

from datetime import datetime
from typing import Dict

from flask import Blueprint, redirect, render_template, request, session, url_for

from .data import (
    ARTIFACTS,
    CATEGORIES,
    COLLECTIONS,
    ISSUES,
    LETTERS,
    PHOTO_ESSAYS,
    REPORTS,
    TAGS,
    USERS,
    ZINES,
    filter_by_category,
    filter_by_tag,
    find_artifact,
    get_authors,
    search_artifacts,
)

public_bp = Blueprint("public", __name__)


@public_bp.context_processor
def inject_globals() -> Dict[str, object]:
    """Inject shared navigation data for templates."""
    return {
        "categories": CATEGORIES,
        "tags": TAGS,
        "issues": ISSUES,
        "authors": get_authors(),
        "current_user": session.get("user"),
    }


@public_bp.route("/")
def home() -> str:
    """Render the central station homepage."""
    editor_pick = ARTIFACTS[0]
    top_article = ARTIFACTS[1]
    recent_articles = ARTIFACTS[-3:]
    return render_template(
        "home.html",
        editor_pick=editor_pick,
        top_article=top_article,
        recent_articles=recent_articles,
        artifacts=ARTIFACTS,
    )


@public_bp.route("/issue/<issue_name>")
def issue(issue_name: str) -> str:
    """Render a monthly issue page with curated routes."""
    issue_data = next((issue for issue in ISSUES if issue.name == issue_name), ISSUES[0])
    issue_artifacts = [artifact for artifact in ARTIFACTS if artifact.issue == issue_data.name]
    return render_template("issue.html", issue=issue_data, artifacts=issue_artifacts)


@public_bp.route("/article/<int:artifact_id>")
def article_detail(artifact_id: int) -> str:
    """Render a standard article page with citations and metadata."""
    artifact = find_artifact(artifact_id)
    if not artifact:
        return redirect(url_for("public.home"))
    return render_template("article.html", artifact=artifact)


@public_bp.route("/report/<int:artifact_id>")
def report_detail(artifact_id: int) -> str:
    """Render investigative report with layered annotations."""
    report = REPORTS.get(artifact_id)
    if not report:
        return redirect(url_for("public.home"))
    return render_template("report.html", report=report)


@public_bp.route("/photo/<int:artifact_id>")
def photo_detail(artifact_id: int) -> str:
    """Render photojournalism viewer with multiple modes."""
    essay = PHOTO_ESSAYS.get(artifact_id)
    if not essay:
        return redirect(url_for("public.home"))
    return render_template("photo.html", essay=essay)


@public_bp.route("/letter/<int:artifact_id>")
def letter_detail(artifact_id: int) -> str:
    """Render letter page with epistolary treatment."""
    letter = LETTERS.get(artifact_id)
    if not letter:
        return redirect(url_for("public.home"))
    return render_template("letter.html", letter=letter)


@public_bp.route("/zine/<int:artifact_id>")
def zine_detail(artifact_id: int) -> str:
    """Render zine reader with matchbox interaction."""
    zine = ZINES.get(artifact_id)
    if not zine:
        return redirect(url_for("public.home"))
    return render_template("zine.html", zine=zine)


@public_bp.route("/category/<category>")
def category_page(category: str) -> str:
    """Render category page styled like a newspaper section."""
    artifacts = filter_by_category(category)
    return render_template("category.html", category=category, artifacts=artifacts)


@public_bp.route("/tag/<tag>")
def tag_page(tag: str) -> str:
    """Render tag page styled like a digest."""
    artifacts = filter_by_tag(tag)
    return render_template("tag.html", tag=tag, artifacts=artifacts)


@public_bp.route("/author/<author_name>")
def author_page(author_name: str) -> str:
    """Render author desk page with curated works."""
    artifacts = [artifact for artifact in ARTIFACTS if author_name in artifact.byline]
    return render_template("author.html", author=author_name, artifacts=artifacts)


@public_bp.route("/library")
def library_page() -> str:
    """Render the library collection interface."""
    collection = COLLECTIONS["Library"]
    artifacts = [artifact for artifact in ARTIFACTS if artifact.id in collection.artifact_ids]
    return render_template("library.html", collection=collection, artifacts=artifacts)


@public_bp.route("/gallery")
def gallery_page() -> str:
    """Render the gallery collection interface."""
    collection = COLLECTIONS["Gallery"]
    artifacts = [artifact for artifact in ARTIFACTS if artifact.id in collection.artifact_ids]
    return render_template("gallery.html", collection=collection, artifacts=artifacts)


@public_bp.route("/map")
def map_page() -> str:
    """Render map page with geotagged artifacts."""
    return render_template("map.html", artifacts=ARTIFACTS)


@public_bp.route("/timeline")
def timeline_page() -> str:
    """Render vertical timeline page with archive navigation."""
    artifacts = sorted(ARTIFACTS, key=lambda artifact: artifact.published)
    return render_template("timeline.html", artifacts=artifacts)


@public_bp.route("/search")
def search_page() -> str:
    """Render advanced search page and results."""
    query = request.args.get("q", "")
    filters = {
        "category": request.args.get("category", ""),
        "location": request.args.get("location", ""),
        "artifact_type": request.args.get("type", ""),
    }
    results = search_artifacts(query, filters) if query else []
    return render_template("search.html", query=query, filters=filters, results=results)


@public_bp.route("/archive")
def archive_page() -> str:
    """Render archive page for monthly issues."""
    return render_template("archive.html", issues=ISSUES)


@public_bp.route("/saved")
def saved_page() -> str:
    """Render saved posts for logged-in users."""
    user_name = session.get("user")
    if not user_name or user_name not in USERS:
        return redirect(url_for("auth.login"))
    user = USERS[user_name]
    saved_artifacts = [artifact for artifact in ARTIFACTS if artifact.id in user.saved]
    return render_template("saved.html", artifacts=saved_artifacts, user=user)


@public_bp.route("/save/<int:artifact_id>", methods=["POST"])
def save_artifact(artifact_id: int) -> str:
    """Save an artifact to a user's reading ledger."""
    user_name = session.get("user")
    if user_name and user_name in USERS:
        user = USERS[user_name]
        if artifact_id not in user.saved:
            user.saved.append(artifact_id)
    return redirect(request.referrer or url_for("public.home"))


@public_bp.route("/favorite/<int:artifact_id>", methods=["POST"])
def favorite_artifact(artifact_id: int) -> str:
    """Favorite an artifact for quick access."""
    user_name = session.get("user")
    if user_name and user_name in USERS:
        user = USERS[user_name]
        if artifact_id not in user.favorites:
            user.favorites.append(artifact_id)
    return redirect(request.referrer or url_for("public.home"))


@public_bp.route("/newsletter", methods=["POST"])
def newsletter_signup() -> str:
    """Accept newsletter signups and redirect with a timestamp.

    This demonstrates a real handler for monthly circulation without persisting
    to an external system yet.
    """
    session["newsletter_last_signed"] = datetime.utcnow().isoformat()
    return redirect(url_for("public.home"))
