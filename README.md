MCrushURL
---------

Very easy to set up. I recommend using virtualenv.

* Clone repository, or download zipball/tarball.
* Run `virtualenv venv`
* Rename config.yml.default to config.yml, edit.
* Run `venv/bin/pip install -r requirements.txt`
* Run `git submodule init`, then `git submodule update`
* Run `venv/bin/twistd -y run.py`
* To monitor the log, use `tail -f twistd.log`

Thanks to @jdiez for https://github.com/MediaCrush/PyCrush
