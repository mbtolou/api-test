# Choosing an API framework for new microservices

This document is intended as a comparison between several Python and Go frameworks that could be considered when building a new Gen3 microservice. Whether to use Python or Go ultimately comes down to personal taste.

## TL;DR

* **Python:** There are plenty of Web frameworks to choose from, and most of them are comparable in performance. Flask is the least performant in a benchmark, but compensates with a big community and a lot of extension options. Many frameworks come with tools to help write an OpenAPI spec that can be used to generate Swagger documentation.

* **Go:** Go already comes with a net/http package that can handle requests. An external framework is not mandatory to write an API in Go, but it makes one's life easier. Go being younger than Python, there are less options and there are no clear winners regarding which are the best. What we need is a router; Gorilla/mux and Gin are the most widely used.

## A summary

| Framework                 | Language               | Pros                                                                                               | Cons                                                                                                                                       |
|------------------|----------------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Flask            | Python 2 and 3 | Popularity, flexible with extension options, well documented                                       | Performance, not async-friendly                                                                                                            |
| Django           | Python 3       | Popularity, customizable, ORM support, complex routing*, well documented                            | Heavy (fullstack not needed), performance, not async-friendly, learning curve                                                              |
| Bottle           | Python 2 and 3 | Popularity, performance, simplicity, no dependencies, complex routing*, well documented             | One-file approach (only good for microservices), not async-friendly (but possible [using gevent](http://bottlepy.org/docs/dev/async.html)) |
| hug              | Python 3       | Popularity, performance, simplicity                                                                | No Swagger tool (but an auto documentation feature), not async-friendly, not very well documented                                          |
| Pyramid          | Python 2 and 3 | Simplicity, performance, complex routing*                                                           | not async-friendly                                                                                                                         |
| API Star         | Python 3       | Performance, well documented                                                                       | Popularity, no Swagger tool (but an auto documentation feature), not async-friendly                                                        |
| Falcon           | Python 2 and 3 | Performance, lightweight, works with async libraries, well documented                              |                                                                                                                                            |
| Quart            | Python 3       | Async, simple evolution from Flask apps, faster than Flask                                         | Not as fast as others, does not support all Flask extensions                                                                               |
| Sanic            | Python 3       | Async, fast, complex routing*, well documented                                                      |                                                                                                                                            |
| Tornado          | Python 2 and 3 | Async, fast, complex routing*                                                                       | Heavy (fullstack not needed)                                                                                                               |
| Standard library | Go             | No external dependencies                                                                           | Tedious                                                                                                                                    |
| Revel            | Go             | Popularity, strong community, well documented                                                      | Heavy (fullstack not needed)                                                                                                               |
| Gorilla/mux      | Go             | Popularity, simple, complex routing*                                                                |                                                                                                                                            |
| Gin              | Go             | Popularity, minimalist, [route grouping feature](https://github.com/gin-gonic/gin#grouping-routes) |                                                                                                                                            |
| Echo             | Go             | Popularity, minimalist, well documented                                                            | Many dependencies                                                                                                                          |
| chi              | Go             | Lightweight, no external dependencies                                                              | Not very well documented                                                                                                                   |
| fasthttprouter   | Go             | Performance                                                                                        | Not very well documented                                                                                                                   |

\* regex allowed in routing

## Python

### Python frameworks

* Tested:
  * [API Star](https://docs.apistar.com/) (not popular enough?) - Python 3+
  * [Bottle](https://bottlepy.org/) (non full stack framework. one-file approach: good for small projects. [list of plugins](http://bottlepy.org/docs/0.12/plugins/index.html)) - Python 2.7 and 3.2+
  * [Falcon](https://falconframework.org/) (non full stack framework. made to build REST APIs) - Python 2 and 3.3+
  * [Flask](http://flask.pocoo.org/) (non full stack framework) - Python 2 and 3.3+
  * [hug](http://www.hug.rest/) (non full stack framework. built on-top of Falcon) - Python 3+
  * [Pyramid](https://trypyramid.com/) (non full stack framework. not popular enough?) - Python 2 and 3.3+
  * [Quart](https://pgjones.gitlab.io/quart/): Flask with asyncio (non full stack framework. Flask apps can easily evolve into Quart apps. async only -> no WSGI) - Python 3.6+
  * [Sanic](https://sanic.readthedocs.io/): async (non full stack framework. [architectural issues](https://github.com/channelcat/sanic/issues/1176)?) - Python 3.5+
  * [Tornado](http://www.tornadoweb.org/) (mostly async) - Python 2 and 3

* Eliminated:
  * [Django](https://www.djangoproject.com/) with the [Django REST Framework](http://www.django-rest-framework.org/) (too heavy. high level, not super performant but has orm)
  * [Japronto](https://github.com/squeaky-pl/japronto) (early preview only. also, did not work well in my tests)
  * [Pycnic](http://pycnic.nullism.com/) (non full stack framework. JSON-API-only)
  * [Sandman 2](https://github.com/jeffknupp/sandman2) (create an API service from an existing database)
  * [Vibora](https://vibora.io/) (async. still in Alpha at this time, but looks like it will be awesome!)
  * [wheezy.web](https://bitbucket.org/akorn/wheezy.web) (full stack framework. version 0.1: too young? also, did not work well in my tests)

* Not tested:
  * [AIOHTTP](https://aiohttp.readthedocs.io/) (mostly async)
  * [CherryPy](https://cherrypy.org/) (non full stack framework. did not work well in my tests)
  * [Cornice](https://cornice.readthedocs.io/) (REST framework for Pyramid)
  * [Eve](http://python-eve.org/) (REST framework built with Flask and MongoDB -> same performance as Flask)
  * [Morepath](https://morepath.readthedocs.io/) (not popular enough?)
  * [Muffin](https://muffin.readthedocs.io/) (not popular enough?)
  * [weppy](http://weppy.org/) (not popular enough?)

Code tested: hello world app. I used [Gunicorn](https://gunicorn.org/). I benchmarked using [wrk](https://github.com/wg/wrk) with 2 threads and keeping 200 HTTP connections open. Some benchmarking results:

```
apistar :    58254 requests in   60s
bottle  :    50772 requests in   60s
falcon  :    46708 requests in   60s
flask   :    25277 requests in   60s
hug     :    48689 requests in   60s
pyramid :    51101 requests in   60s
quart   :    47949 requests in   60s
sanic   :   143127 requests in   60s
tornado :   139741 requests in   60s

apistar :   659783 requests in  600s
bottle  :   584356 requests in  600s
falcon  :   606565 requests in  600s
flask   :   367817 requests in  600s
hug     :   498142 requests in  600s
pyramid :   557527 requests in  600s
quart   :   480928 requests in  600s
sanic   :  1766532 requests in  600s
tornado :  1476303 requests in  600s
```

Note: I used Gunicorn Quart workers for Quart, [Gunicorn Sanic workers](https://sanic.readthedocs.io/en/latest/sanic/deploying.html#running-via-gunicorn) for Sanic and Gunicorn Tornado workers for Tornado.

[This benchmark by the creator of Quart](https://gitlab.com/pgjones/quart-benchmark) is intended as a comparison between Flask and Quart, and also includes Sanic and AIOHTTP. The results I obtained:

```
Benchmark duration: 30s for each framework
#################################################################################
get requests/second
████                                                 773  flask                  
████████                                            1411  quart                  
█████████                                           1552  quart-daphne           
████████████                                        2036  quart-hypercorn        
█████████████                                       2211  quart-gunicorn         
███████████████                                     2668  flask-gunicorn-eventlet
████████████████                                    2719  quart-gunicorn-uvloop  
████████████████████████                            4094  quart-uvicorn          
██████████████████████████                          4522  aiohttp                
█████████████████████████████████                   5634  flask-gunicorn-meinheld
██████████████████████████████████████████████      7858  aiohttp-gunicorn-uvloop
█████████████████████████████████████████████████   8405  sanic-gunicorn-uvloop  
██████████████████████████████████████████████████  8467  sanic                  
#################################################################################
post requests/second
██                                                   422  flask                  
████████                                            1270  quart-daphne           
█████████                                           1344  quart                  
█████████████                                       1952  quart-gunicorn         
█████████████                                       1968  quart-hypercorn        
█████████████                                       2024  flask-gunicorn-eventlet
███████████████                                     2265  quart-gunicorn-uvloop  
██████████████████████                              3260  quart-uvicorn          
█████████████████████████                           3702  flask-gunicorn-meinheld
████████████████████████████                        4083  aiohttp                
███████████████████████████████████████████████     6897  aiohttp-gunicorn-uvloop
█████████████████████████████████████████████████   7248  sanic-gunicorn-uvloop  
██████████████████████████████████████████████████  7259  sanic
```

**Conclusion:** Flask is the least performant framework in my tests. Quart is more performant than Flask, but is outperformed by the other frameworks. Bottle, Falcon, hug and Pyramid seem to have a similar performance. API Star seems slightly more performant.

### Swagger tools

At this date, the latest Swagger version is version 3.18.3 (released on 08/03/2018). A list of community-driven Swagger frameworks can be found [here](https://swagger.io/tools/open-source/open-source-integrations/). The Swagger tool [swagger-codegen](https://github.com/swagger-api/swagger-codegen) (Swagger version 2.3) can be used to generate documentation from an OpenAPI spec file.

Some tools to help writing the OpenAPI spec:

* API Star: supports the [automatic generation of OpenAPI 3.0 schemas](https://docs.apistar.com/api-guide/api-schemas/) (this is not well documented so hard to use). In beta: the schema can be kept in sync with GitHub via a [config file](https://www.apistar.com/pages/docs).
* Bottle: [apispec](https://github.com/marshmallow-code/apispec). validation with [bottle-swagger](https://github.com/ampedandwired/bottle-swagger)
* Falcon: [falcon-swagger](https://github.com/dutradda/falcon-swagger)
* Flask: [flask-swagger](https://github.com/gangverk/flask-swagger) (Swagger 2.0) or [safrs](https://github.com/thomaxxl/safrs) or [apispec](https://github.com/marshmallow-code/apispec)
* hug: no external tool. hug can auto-generates documentation from docstrings, but the functionality is not well documented
* Pyramid: [pyramid_apispec](https://github.com/ergo/pyramid_apispec). validation with [pyramid_swagger](https://github.com/striglia/pyramid_swagger)
* Quart: [quart-openapi](https://github.com/factset/quart-openapi)
* Sanic: [sanic-openapi](https://github.com/channelcat/sanic-openapi)
* Tornado: [tornado-swagger](https://github.com/SerenaFeng/tornado-swagger) or [apispec](https://github.com/marshmallow-code/apispec)

**Conclusion:** At this date, there are tools to help write an OpenAPI schema for all frameworks, except API Star and hug. API Star supports automatic generation of OpenAPI schemas, but it looks like the functionality is not fully developed yet and documentation is hard to find.

### ORM libraries

* API Star: supports Django ORM and SQLAlchemy. A library: [apistar-sqlalchemy](https://github.com/PeRDy/apistar-sqlalchemy). A SQLAlchemy discussion [here](https://github.com/encode/apistar/issues/546)
* Bottle: SQLAlchemy with the [bottle-sqlalchemy](https://github.com/iurisilvio/bottle-sqlalchemy) plugin. SQLite with the [bottle-sqlite](http://bottlepy.org/docs/0.12/plugins/sqlite.html) plugin or the [Macaron](http://nobrin.github.io/macaron/webapp.html) plugin
* Falcon: SQLAlchemy with [middleware](https://eshlox.net/2017/07/28/integrate-sqlalchemy-with-falcon-framework/)
* Flask: SQLAlchemy
* Pyramid: [supports SQLAlchemy](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/database/sqlalchemy.html)
* Quart: SQLAlchemy because [Quart supports some Flask extensions](https://pgjones.gitlab.io/quart/flask_extensions.html)
* Sanic: SQLAlchemy. Some examples [here](https://github.com/seanpar203/sanic-starter) and [here](https://github.com/easydaniel/sanic-example)
* Tornado: [aiopg](https://aiopg.readthedocs.io/en/stable/index.html), which can support SQLAlchemy

### Compare using a real Gen3 endpoint

The Gen3 microservice pidgin is a Flask app that sends requests to peregrine. I transformed it into an API Star app, a Bottle app and a Falcon app. The structure of a Falcon app is slightly different, so more changes were required than when transforming it into an API Star or a Bottle app. In all cases, the performance variation is very small, probably because the bottleneck is not pidgin but peregrine.

Some benchmarking results (with Gunicorn and wrk):

```
apistar :       64 requests in   60s
bottle  :       62 requests in   60s
falcon  :       64 requests in   60s
flask   :       61 requests in   60s
```

### Python frameworks conclusion

* **Flask** is popular. It has a big community and a lot of extension options, including Swagger generation options. However, all the other frameworks I tested beat Flask in performance and it is not async-friendly.
* We can use **Quart (async)** if we want better performance without making a big change from Flask, which we currently use. Quart allows using the async features of Python 3.6+. It provides an easy way for converting existing Flask apps into async apps: find and replace "flask" with "quart" and add the "async" and "await" keywords where appropriate.
* For microservices, **Bottle** also looks promising (better performance than Flask, an SQLAlchemy plugin and a Swagger helper tool) and is simple to write, but may not be a fit if the project becomes bigger than a microservice. **Falcon** and **Pyramid** are good options too.
* **API Star** is slightly faster, but does not provide an easy way to generate Swagger documentation.
* For speed: **Sanic or Tornado (async)**. Though for a microservice that doesn't need async, they may not be the right choice because other frameworks can offer more features.

## Go

### Go frameworks

Go comes with the [net/http package](https://golang.org/pkg/net/http/) that can handle requests. For better performance, we can use the [fasthttp](https://github.com/valyala/fasthttp) package (designed to be 10 times faster than net/http).

Since Go already handles requests, we're looking for a framework that provides a routing system. A list of Web frameworks for Go ordered by popularity on GitHub can be found [here](https://github.com/mingrammer/go-web-framework-stars). A lit of Go routers can be found [here](https://github.com/avelino/awesome-go#routers).

* Considered:
  * It's possible to do it with the standard Go library. An example [here](https://ryanmccue.ca/how-to-create-restful-api-golang-standard-library/)
  * [chi](https://github.com/go-chi/chi) (lightweight http router. no external dependencies. the documentation isn't very good)
  * [Gin](https://gin-gonic.github.io/gin/) (popular, fast and minimalist. [route grouping feature](https://github.com/gin-gonic/gin#grouping-routes). good for a small project)
  * [Gorilla/mux](http://www.gorillatoolkit.org/pkg/mux) (popular, simple. a lot of routing features, such as subrouters and regex matching)
  * [Gorilla/pat](http://www.gorillatoolkit.org/pkg/pat) (more lightweight than Gorilla/mux?)
  * [fasthttprouter](https://github.com/buaazp/fasthttprouter) uses fasthttp
  * [Echo](https://echo.labstack.com/) (minimalist. good documentation. a lot of dependencies)

* Too heavy for our needs in a microservice:
  * [Beego](https://beego.me/): (heavy and no community. Some scalabitity problems. Has ORM and "bee tool" for auto function calls when codebase changes. [Swagger is integrated in beego 1.3 -> auto generated api document](https://beego.me/blog/beego_api), though it doesn't seem very stable as can be seen in the comments)
  * [Buffalo](https://gobuffalo.io/)
  * [go-restful](https://github.com/emicklei/go-restful)
  * [Revel](https://revel.github.io/) (heavy. strong community base. no native MongoDB support)

* Not considered:
  * [bone](https://github.com/go-zoo/bone) because it is not popular enough
  * [goa](https://goa.design/) (design-first framework -> the generation of a Swagger spec file is included) because it is not popular enough
  * [Goji](https://goji.io/) (websocket support but doesn't add a lot to standard Go) because it is not popular enough
  * [Iris](https://iris-go.com/) because of [these issues](http://www.florinpatan.ro/2016/10/why-you-should-not-use-iris-for-your-go.html)
  * [Martini](https://github.com/go-martini/martini) (good router. about 40 times slower than Gin. in general, not a great performance) because it is slow and no longer maintained
  * [Pat](https://github.com/bmizerany/pat) because it is no longer maintained
  * [routes](https://github.com/drone/routes) because it is deprecated
  * [Web.go](https://github.com/bnkamalesh/webgo) (minimalist. tree routing makes it efficient. doesn't add a lot to standard Go) because it is not popular enough

Two benchmarks [here](https://github.com/julienschmidt/go-http-routing-benchmark) and [here](https://github.com/smallnest/go-web-framework-benchmark).

### Swagger tools

* [go-swagger](https://github.com/go-swagger/go-swagger) (Swagger 2.0) can [generate a Swagger spec from the source code](https://goswagger.io/generate/spec.html). Step by step [here](https://www.ribice.ba/swagger-golang/)
* net/http, Echo and Gin are supported by [swag](https://github.com/swaggo/swag)
* chi can auto generate documentation but [it is not quality API documentation](https://github.com/go-chi/chi/issues/180) and there is no tool to generate an OpenAPI spec
* go-restful documentation with [go-restful-openapi](https://github.com/emicklei/go-restful-openapi)

### ORM libraries

A lit of ORM libraries can be found [here](https://github.com/avelino/awesome-go#orm). Go comes with the [database/sql package](https://golang.org/pkg/database/sql/). The following are extensions on top of the database/sql package that make it more developer-friendly:

* [gorm](http://gorm.io/)
* [sqlx](https://godoc.org/github.com/jmoiron/sqlx)
* [dbr](https://github.com/gocraft/dbr)

### Testing options

Go comes with a built-in unit test package called [testing](https://golang.org/pkg/testing/). Examples [here](https://blog.alexellis.io/golang-writing-unit-tests/).

### Go frameworks conclusion

* **Gorilla/mux** is a good option for a microservice, especially if we need some of the many routing possibilities it supports.
* **Gin** and **Echo** have a strong community and could be good options as well for routing in a microservice (lightweight, fast, can be used with gorm, there's a Swagger generation tool).
* For speed: **fasthttprouter**.
