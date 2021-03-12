# RTX Scalping

This is a python app developed for deployment on Heroku.
It queries power.dk's website for RTX 3060ti, 3070 and 3080 in stock.
If in stock it will send notification via Spontit, and show up on the web app.

## Bootstrap
You need to fork this repo if you want github integration to push directly on changes, otherwise this is a way to get started with a local heroku git:

    git clone https://github.com/axlroden/rtxscalping.git
    cd rtxscalping
    rm -rf .git
    heroku login
    heroku create rtxscapling --region eu
    heroku addons:create heroku-redis --app rtxscalping
    # This is just for better logging:
    heroku addons:create papertrail --app rtxscalping
    # Set environment variables
    heroku config:set POWER_URL=https://www.power.dk/umbraco/api/product/getproductsbysearchrequest?cat=1344&f-1-100510=GeForce%20RTX%203060%20Ti&f-1-100510=GeForce%20RTX%203070&f-1-100510=Geforce%20RTX%203080&from=0&s=5&size=36&nocache=
    heroku config:set SPONTIT_KEY=YourSpontitApiKey
    heroku config:set SPONTIT_INVITE_URL=YourInviteUrl
    # For responder to function on free dynos
    heroku config:set WEB_CONCURRENCY=1

## Deploy
    git init
    git add .
    git commit -am "Initial release"
    git push heroku master

## Start app:
    heroku ps:scale web=1
    heroku ps:scale clock=1





