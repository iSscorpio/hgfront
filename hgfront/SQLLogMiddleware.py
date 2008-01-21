"""
$Id: SQLLogMiddleware.py 306 2007-10-22 14:55:47Z tguettler $

This middleware
in settings.py you need to set

DEBUG=True
DEBUG_SQL=True

# Since you can't see the output if the page results in a redirect,
# you can log the result into a directory:
# DEBUG_SQL='/mypath/...'

MIDDLEWARE_CLASSES = (
	'YOURPATH.SQLLogMiddleware.SQLLogMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	...)

Slightly modified from original by Rob van der Linde <robvdl@gmail.com>

	- Now supports XHTML content types
	- Now generates a nice dropdown window/banner at the top of the page.
	  Only works in Firefox (and other standards compliant browsers), but
	  then, no serious developers use IE anyway...

"""

import re, os, time, datetime
from django.conf import settings
from django.db import connection
from django.template import Template, Context

_HEAD_SECTION_RE = re.compile(r'(</head.*>)', re.DOTALL)
_BODY_SECTION_RE = re.compile(r'(<body.*?>)', re.DOTALL)

class SQLLogMiddleware:
	start = None

	def process_request(self, request):
		self.start = time.time()

	def process_response (self, request, response):
		# self.start is empty if an append slash redirect happened.
		debug_sql = getattr(settings, "DEBUG_SQL", False)
		if (not self.start) or not (settings.DEBUG and debug_sql):
			return response
		timesql = 0.0
		for q in connection.queries:
			timesql += float(q['time'])
			seen = {}
			duplicate = 0
		for q in connection.queries:
			sql = q["sql"]
			c = seen.get(sql, 0)
			if c:
				duplicate += 1
			q["seen"] = c
			seen[sql] = c + 1
		t = Template('''
			<div id="sqllog">
				<span><a href="javascript:activate_slider();"><strong>Django SQL log for this page: click to toggle</strong></a></span>
				<div>
					<p>
						<strong>request.path:</strong> {{ request.path|escape }}<br />
						<strong>Total query count:</strong> {{ queries|length }}<br />
						<strong>Total duplicate query count:</strong> {{ duplicate }}<br />
						<strong>Total SQL execution time:</strong> {{ timesql }}<br />
						<strong>Total Request execution time:</strong> {{ timerequest }}<br />
					</p>
					<table border="0" cellspacing="0">
						<tr>
							<th>Time</th>
							<th>Frequency</th>
							<th>SQL</th>
						</tr>
						{% for sql in queries %}
							<tr>
								<td>{{ sql.time }}</td>
								<td class="alright">{{ sql.seen }}</td>
								<td>{{ sql.sql }}</td>
							</tr>
						{% endfor %}
					</table>
					{% if duplicate %}
						<p>To avoid duplicates, read: <a href="http://www.djangoproject.com/documentation/db-api/#caching-and-querysets" target="_blank">Caching and Querysets</a>.</p>
					{% endif %}
					<p><button onclick="about_sql_debug()">About</button></p>
				</div>
			</div>
		''')
		c = Template(r'''
			<style type="text/css">
				/*<![CDATA[*/
					/* I use the !important keyword on just about any element
					   here, mainly as a precaution. Since we want this to work
					   with any web page (if possible), We should make sure other
					   CSS styles from the underlying page do not interfere with
					   the infobar. This should work on _most_ webpages, but I do
					   expect that in some cases, you may need to add some minor
					   corrections in your site's CSS file. This is, only if some
					   of your styles are interfering with the infobar's styles.
					   Also, this thing is only expected to work in Firefox, and
					   other CSS compliant browsers, Opera, Safari, Konqueror, etc.
					   Most web developers don't use IE anyway, which is who this
					   middleware is aimed at. It's not recommended to run on
					   production sites for security.
					*/

					html {
						padding-top: 24px !important;
					}

					#sqllog {
						font: normal 11px "MS Sans Serif", sans !important;
						color: black !important;
						background: #ffffe1 !important;
						position: fixed !important;
						top: 0 !important;
						left: 0 !important;
						width: 100% !important;
						height: 24px !important;
						border-bottom: 2px outset !important;
						z-index: 255 !important;
						overflow: hidden !important;
					}

					#sqllog div {
						overflow: auto !important;
						height: 276px !important;
					}

					#sqllog.slideropen {
						height: 300px !important;
					}

					html.slideropen {
						padding-top: 300px !important;
					}

					#sqllog table, #sqllog tr, #sqllog td, #sqllog th {
						border: none !important;
					}

					#sqllog table {
						margin: 0 4px !important;
					}

					#sqllog th {
						padding-right: 20px !important;
						font: bold 8px "MS Sans Serif", sans !important;
					}

					#sqllog .alright {
						padding-right: 20px !important;
						text-align: right !important;
					}

					#sqllog span a {
						color: black !important;
						display: block !important;
						padding: 5px 4px 0 26px !important;
						height: 19px;
						background-image: url('/media/images/infobar_icon.png') !important;
						background-repeat: no-repeat !important;
						background-position: 4px 3px !important;
						cursor: default !important;
						text-decoration: none !important;
					}

					#sqllog span a:hover {
						text-decoration: none !imporant;
						color: HighlightText !important;
						background-color: Highlight !important;
					}

					#sqllog a {
						color: #5b80b2 !important;
						text-decoration: none !imporant;
					}

					#sqllog a:hover {
						color: #003366 !important;
						text-decoration: none !imporant;
					}

					#sqllog p {
						margin: 12px 4px 12px 4px !important;
					}

					#sqllog p strong {
						display: block !important;
						float: left !important;
						width: 220px !important;
					}
				/*]]>*/
			</style>
			<script type="text/javascript">
				//<![CDATA[
					function activate_slider()
					{
						var sqllogClass = document.getElementById('sqllog').className
						var htmlClass = document.getElementsByTagName('html')[0].className;
						if (sqllogClass.search(/slideropen/) == -1)
						{
							document.getElementById('sqllog').className += ' slideropen';
							document.getElementsByTagName('html')[0].className += ' slideropen';
						}
						else
						{
							sqllogClass = sqllogClass.replace(/slideropen/, '');
							htmlClass = htmlClass.replace(/slideropen/, '');
							document.getElementById('sqllog').className = sqllogClass;
							document.getElementsByTagName('html')[0].className = htmlClass;
						}
					}

					function about_sql_debug()
					{
						alert('Django SQL Debugger 0.1\\n\\nA free middleware (filter), for use in any Django application. Shows the SQL queries generated by your web applications in realtime, using an \'IE style\' collapsable infobar at the top of every page. To get rid of this bar, the web developer should disable this middleware from the web application\\'s settings.py file.\\n\\nOriginal code "SQLLogMiddleware + duplicates", from Django Snippet #344, by "guettli".\\nModifications & Javascript + CSS implementation of the Infobar by Rob van der Linde.\\n\\nUnknown Licence, I would like to go with BSD, but that depends on the original author\'s Licence.');
					}
				//]]>
			</script>
		''')
		timerequest = round(time.time() - self.start, 3)
		queries = connection.queries
		html = t.render(Context(locals()))
		css = c.render(Context(locals()))
		if debug_sql == True:
			if response.get("content-type", "").startswith("text/html") or response.get("content-type", "").startswith("application/xhtml+xml"):
				tag = _BODY_SECTION_RE.search(response.content)
				if tag:
					response.content = _BODY_SECTION_RE.sub(tag.group(0) + html, response.content)
					tag = _HEAD_SECTION_RE.search(response.content)
					if tag:
						response.content = _HEAD_SECTION_RE.sub(css + tag.group(0), response.content)
			return response
		assert os.path.isdir(debug_sql), debug_sql
		outfile = os.path.join(debug_sql, "%s.html" % datetime.datetime.now().isoformat())
		fd = open(outfile, "wt")
		fd.write('''<html><head><title>SQL Log %s</title></head><body>%s</body></html>''' % (request.path, html))
		fd.close()
		return response
