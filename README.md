lxmlbind
=========

Python LXML object binding.

[![Build Status](https://travis-ci.org/jessemyers/lxmlbind.png)](https://travis-ci.org/jessemyers/lxmlbind)

What is this?
-------------

The [xml.etree][1] library is a great way to manipulate XML in Python, but in most domains
it is clearer to use objects that model your domain entities instead of manipulating
the XML representation directly. The motivating example was [Jenkins][2] XML job
configurations, but the same problem is likely to exist for any XML-based modeling.

This project attempts to use Python [data descriptors][3] to bind an element tree
to Python objects.

 [1]: http://lxml.de/tutorial.html
 [2]: http://jenkins-ci.org/
 [3]: http://docs.python.org/2/howto/descriptor.html

Example
-------

Assume that you have an API using XML representations of people with first and last names:

     xml = "<person><first>John</first><last>Doe</last></person"

*lxmlbind* makes it easy to define a `Person` object that maps to this structure:

    from lxmlbind.api import Base, Property

    class Person(Base):
        first = Property("first")
        last = Property("last")

Instances of `Person` wrap an `lxml.etree` and support manipulation of this structure
through instance attributes:

     # create the person from XML
     person = Person.from_xml(xml)
     
     # get the first name attribute
     assert person.first == "John"
     
     # set the last name attribute
     person.last = "Smith"
     
     # print the resulting XML
     print person.to_xml()
     
     # delete the first name entirely
     del person.first
