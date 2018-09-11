# Choosing a default API framework for new microservices

## Python

### Python frameworks

* Tested:
  * API Star (not popular enough?) - Python 3+
  * Bottle - Python 2.7 and 3.2+
  * Falcon - Python 2 and 3.3+
  * Flask - Python 2 and 3.3+
  * hug (built on-top of Falcon) - Python 3+
  * Pyramid (not popular enough?) - Python 2 and 3.3+
  * Sanic ([architectural issues](https://github.com/channelcat/sanic/issues/1176)) - Python 3.5+

Code tested: hello world app. I used [Gunicorn](https://gunicorn.org/) (with [Gunicorn sanic workers](https://sanic.readthedocs.io/en/latest/sanic/deploying.html#running-via-gunicorn) for sanic). I benchmarked using [wrk](https://github.com/wg/wrk) with 2 threads and keeping 200 HTTP connections open. Some benchmarking results:

```
apistar :    58254 requests in   60s
bottle  :    50772 requests in   60s
falcon  :    46708 requests in   60s
flask   :    25277 requests in   60s
hug     :    48689 requests in   60s
pyramid :    51101 requests in   60s
sanic   :   143127 requests in   60s

apistar :   659783 requests in  600s
bottle  :   584356 requests in  600s
falcon  :   606565 requests in  600s
flask   :   367817 requests in  600s
hug     :   498142 requests in  600s
pyramid :   557527 requests in  600s
sanic   :  1766532 requests in  600s
```

Note: the results obtained with Sanic are not comparable to the others because the workers are different.

* Eliminated:
  * AIOHTTP (mostly async)
  * Django with the Django REST Framework (too heavy. not super performant but has orm)
  * Japronto (early preview only. also, did not work)
  * Pycnic (JSON-API-only)
  * Quart (Flask apps can evolve into Quart apps. better performance than Flask? but async only -> no WSGI)
  * Sandman (no code, admin page)
  * wheezy.web (version 0.1: too young? also, did not work)

* Not tested:
  * CherryPy (did not work)
  * Cornice (REST framework for Pyramid)
  * Eve (REST framework built with Flask and MongoDB -> same performance as Flask)
  * Morepath (not popular enough?)
  * Muffin (not popular enough?)
  * Restless (framework agnostic. use the same API code for Django, Flask, Bottle...)
  * Tornado (mostly async)
  * weppy (not popular enough?)

**Conclusion:** Flask is the most supported but the least performant in the benchmark. Bottle, Falcon, hug and Pyramid seem to be equally performant. API Star seems slightly more performant. Sanic is eliminated because of architectural issues and because it's hard to compare it to the other frameworks.

### Swagger tools

At this date, the latest Swagger version is version 3.18.3 (released on 08/03/2018). A list of community-driven Swagger frameworks can be found [here](https://swagger.io/tools/open-source/open-source-integrations/). The Swagger tool [swagger-codegen](https://github.com/swagger-api/swagger-codegen) (Swagger version 2.3) can be used to generate documentation from an OpenAPI spec file.

Some tools to help writing the OpenAPI spec:

* API Star: supports the [automatic generation of OpenAPI 3.0 schemas](https://docs.apistar.com/api-guide/api-schemas/) (this is not documented enough so hard to use). In beta: the schema can be kept in sync with GitHub via a [config file](https://www.apistar.com/pages/docs).
* Bottle: [apispec](https://github.com/marshmallow-code/apispec). validation with [bottle-swagger](https://github.com/ampedandwired/bottle-swagger) (Swagger 2.0)
* Falcon: [falcon-swagger](https://github.com/dutradda/falcon-swagger) (Swagger 2.0)
* Flask: [flask-swagger](https://github.com/gangverk/flask-swagger) (Swagger 2.0) or [safrs](https://github.com/thomaxxl/safrs) or [apispec](https://github.com/marshmallow-code/apispec)
* hug: no tool
* Pyramid: [pyramid_apispec](https://github.com/ergo/pyramid_apispec). validation with [pyramid_swagger](https://github.com/striglia/pyramid_swagger) (Swagger 2.0)
* Sanic: [sanic-openapi](https://github.com/channelcat/sanic-openapi)

**Conclusion:** There are tools to help write a JSON schema for Bottle, Falcon, Flask, Pyramid and Sanic. There is no tool to generate OpenAPI documentation for hug. API Star supports automatic generation of OpenAPI schemas, but it looks like the functionality is not fully developed yet and documentation is hard to find.

### ORM libraries

* API Star: supports Django ORM and SQLAlchemy. A library: [apistar-sqlalchemy](https://github.com/PeRDy/apistar-sqlalchemy). A SQLAlchemy discussion [here](https://github.com/encode/apistar/issues/546)
* Bottle: SQLAlchemy. A plugin: [bottle-sqlalchemy](https://github.com/iurisilvio/bottle-sqlalchemy)
* Falcon: SQLAlchemy with [middleware](https://eshlox.net/2017/07/28/integrate-sqlalchemy-with-falcon-framework/)
* Flask: SQLAlchemy
* Pyramid: [SQLAlchemy](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/database/sqlalchemy.html)
* Sanic: SQLAlchemy. Some examples [here](https://github.com/seanpar203/sanic-starter) and [here](https://github.com/easydaniel/sanic-example)

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

Flask has a bigger community, as well as more Swagger generation options than the other frameworks, but they all beat it in performance. Bottle looks promising (good performance, SQLAlchemy plugin and a Swagger generation tool).

## Go

### Go frameworks

Go comes with a net/http package that can handle requests. We're looking for a framework that provides a routing system.

* Native Go. Example [here](https://ryanmccue.ca/how-to-create-restful-api-golang-standard-library/)
* Revel (heavy. strong community base. no native MongoDB support)
* Gin (not good for apps with a big backend or complex functions)
* Martini (40x slower than Gin. in general, not a great performance)
* Web.go (doesn't add a lot to standard Go)
* Gorilla (popular, out of the box not very performant, but can be configured)
* Gorilla pat (lightweight)
* Goji (websocket support but doesn't add a lot to standard Go)
* Beego: heavy and no community. Some scalabitity problems. Has ORM and "bee tool" (auto function calls when codebase changes). [Swagger is integrated in beego 1.3 -> auto generated  api document](https://beego.me/blog/beego_api), though it doesn't seem very stable as can be seen in the comments
* Buffalo
* Echo
* Iris
* goa: design-first framework
* chi: http router
* fasthttp

Two benchmarks [here](https://github.com/julienschmidt/go-http-routing-benchmark) and [here](https://github.com/smallnest/go-web-framework-benchmark).

### Swagger tools

* [go-swagger](https://github.com/go-swagger/go-swagger) (Swagger 2.0) can [generate a Swagger spec from the source code](https://goswagger.io/generate/spec.html). Step by step [here](https://www.ribice.ba/swagger-golang/)
* [swag](https://github.com/swaggo/swag) supports Gin, Echo and net/http
* The generation of a Swagger spec file is included in goa

### Testing

Go comes with a built-in unit test package called [testing](https://golang.org/pkg/testing/). Examples [here](https://blog.alexellis.io/golang-writing-unit-tests/).

### Go frameworks conclusion

I think Gin would be a good option for a microservice (lightweight, fast, can be used with gorm ORM, there's a Swagger generation tool).
