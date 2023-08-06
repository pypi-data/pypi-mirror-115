======
papyru
======

A minimal toolset to help developing RESTful services on top of django.

Tests
=====

While development, you can simply run `make test` or `./run test locally`.
Test requirements are installed into test-env/ if not already present.
It is highly recommended to finally run the containerized tests to ensure
compatiblity to the Python versions we use in our projects.

Requirements
============

- cerberus is used for userdefined validation of models.

Components
==========

The project is split in several mostly independent components.

Context
-------

A context parses input from the client and creates HTTP responses given a
response object, status and headers. The input and response object are encoded
and decoded according to the context.

Example:
          class ExampleResource(Resource):
              def post(self, request):
                  ctx = JSONContext(request)

                  return ctx.response(
                      body={'echo': ctx.data['user_message'],
                            status=HTTPStatus.CREATED,
                            headers={'some-header': 'example'}})

Problem
-------

Problems are objects representing some failure that causes the processing of
the current request to be canceled. They are intended to be reported to the
user given an HTTP error code, title and description. When used with Resources,
they can be thrown as exceptions.

You can construct a Problem object for every HTTP error code defined in
`http.HTTPStatus` by calling `Problem.error_status_code_in_lowercase(...)`.

Examples:

- HTTPStatus.BAD_REQUEST (400):

  .. code-block:: python

    raise Problem.bad_request(detail="I don't like it.")

- HTTPStatus.INTERNAL_SERVER_ERROR (500):

  - **DEPRECATED**:

     .. code-block:: python

       raise Problem.internal_error(detail="Sorry, I still don't like it.")

  - recommended:

     .. code-block:: python

       raise Problem.internal_server_error(
           detail="Sorry, I still don't like it.")

- HTTPStatus.NOT_IMPLEMENTED (501):

  .. code-block:: python

    raise Problem.not_implemented()

Resource
--------

A base class for RESTful resource implementations to be used as Django views.
Dispatching is handled based on the HTTP method of the request. When handling a
request, the instance-method named exactly like the lowercase version of the
HTTP method is called. The response depends on the control flow of the specific
handler. If it returns normally, whatever value is returned from the handler is
the response. Otherwise the Resource tries to emit a meaningful error message.

- If a Problem was raised, it is returned as a response.
- If an ObjectDoesNotExist exception was raised, a Problem.not_found instance is
  returned.
- Otherwise the exception is wrapped in a Problem.internal_error

All Problems belonging to the 5XX-class of HTTP errors are logged to stdout.


Serializers
-----------

Serializers are used to translate objects from transport to internal
representation and back. Both representations can be chosen freely.

A serializer can be constructed with either an internal representation, a
transport representation or both. Internal as well as transport representation
can be queried after construction. To define the transition between
representations a specific serializer needs to implement the to_instance,
to_representation and merge methods. When both representations are given at
construction, the merge method is called.

Validators
----------

When a transport representation is given it can be validated during
construction.

Validation is defined by a validator, given by the validator field of the
serializer. This field can hold a reference to an object that implements a
validate method. When this method is called with a transport representation it
should either return a normalized version of the representation or raise an
error.

Predefined validators are the CerberusValidator and the JSONSchemaValidator.
The CerberusValidator checks objects against a cerberus schema definition. The
JSONSchemaValidator checks against JSON Schemes.

Logger
-------

The LogSquence can be used, to create a easy human readable logging trace.

**Example Call:**

.. code-block:: python

  with LogSequence('foobar') as log:
      log.info('foobar started')
      log.warn('something is not perfect')
      with LogSequence('bar') as lo:
          lo.ok('child logging')
      with LogSequence('foo') as lo:
          lo.fail('foo failed')
          raise Exception('Something went wrong..')

**Example Output:**

::

  ⚫ foobar
     - foobar started
     ⚠ something is not perfect
     ⚫ bar
        ✓ child logging
        ☀ succeeded
     ⚫ foo
        ✗ foo failed
        ☇ failed
           ↪ foobar.py l.11 | raise Exception('Something went wrong..')
           ↪ Exception: Something went wrong..
     ☇ failed
        ↪ foobar.py l.11 | raise Exception('Something went wrong..')
        ↪ Exception: Something went wrong..

Utils
-----
- limited_runtime: checks if runtime is left. Example::

    with limited_runtime(
            datetime.timedelta(minutes=MAX_RUNTIME_MINUTES)
    ) as has_runtime_left:
        while has_runtime_left():
            do_something()
            sleep(1)

Scripts
-------
- generate_jsonschema.py:
  Generates JSON Schemas for the schemas of the transmitted Swagger 3.X.X file.
