# -- FILE: features/steps/compress_steps.py
from behave import given, when, then, step
import tarfile
import sys
sys.path.append("..")
from compress import Compress

# Feature: Creating and writing with a Compress object
@given('we want to compress some files')
def step_impl(context):
    context.filename = "behave_compress_test"
    context.exc = None

@when('we create the object with the extension {extension}')
def step_impl(context, extension):
    try:
        context.object = Compress(extension, context.filename)
    except Exception as e:
        context.exc = e

@when('we have an open file for writing')
def step_impl(context):
    context.execute_steps('''
        When we create the object with the extension .tgz
    ''')

@when('we add the folder {foldername} to the archive')
def step_impl(context, foldername):
    try:
        context.object.add('/'.join(['features', foldername]))
    except Exception as e:
        context.exc = e

@when('we archive the folder {foldername} to the archive')
def step_impl(context, foldername):
    try:
        context.object.add('/'.join(['features', foldername]))
    except Exception as e:
        context.exc = e

@then('a new tarfile should open for writing')
def step_impl(context):
    assert context.object is not None

@then('the archive should contain {filename}')
def step_impl(context, filename):
    context.object.close()
    arcfile = tarfile.open('.'.join([context.filename, 'tar.gz']), 'r')
    member = None
    try:
        member = arcfile.getmember('/'.join([context.filename, filename]))
    except Exception as e:
        context.exc = e
    assert member is not None

@then('the Compress object can be removed')
def step_impl(context):
    context.object.close()
    context.object.delete()

@then('a {type} exception should occur')
def step_impl(context, type):
    assert isinstance(context.exc, eval(type))

