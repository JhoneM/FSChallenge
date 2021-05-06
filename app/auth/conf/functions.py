import functools
from flask import (
    g,
    url_for,
    redirect,
)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def check_level(view):
    @functools.wraps(view)
    def wrapped_views(**kwargs):
        if g.user["level_id"] != 1:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_views
