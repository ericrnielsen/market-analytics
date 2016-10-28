#!/usr/bin/python


import web
import menu_options
from Article import Article
from Article_List import Article_List

class index:
    def GET(self):
        return "Hello, world!"

class form:
    form = web.form.Form(
        web.form.Checkbox('LoadArticles', value=True),
        web.form.Checkbox('Determine Top Tickers', value=True),
        web.form.Checkbox('View Ticker List', value=True),
        web.form.Checkbox('Edit Ticker List', value=True),
        web.form.Checkbox('Get Market Data', value=True),
        web.form.Button('Post entry')
    )

    # GET method is used when there is no form data sent to the server
    def GET(self):
        form = self.form()
        return render.form(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            print 'uh oh'
    	master_articles = Article_List()
    	master_tickers = []
    	master_stock_data = []
    	master_articles, master_articles_description, master_tickers =  \
		menu_options.load_articles(master_tickers)
        print master_tickers
        raise web.seeother('/success')


if __name__ == "__main__":

    urls = (
        '/articles', 'form',
        '/success', 'index'
    )

    render = web.template.render('templates/')

    app = web.application(urls, globals())
    app.run()