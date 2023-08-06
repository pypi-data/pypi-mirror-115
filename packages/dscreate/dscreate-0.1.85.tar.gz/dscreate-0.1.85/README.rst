.. dscreate documentation master file, created by
   sphinx-quickstart on Wed Apr 28 17:16:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================
`dscreate`
====================================

*Flatiron Iron School Data Science Toolkit*

`Read the docs <https://dscreate.readthedocs.io/>`_


Installation
============
* run ``pip install dscreate``

Table of Contents
==================

* `CLI Tools <#cli-tools>`_
* `Creating a Lesson <#creating-a-lesson>`_
* `Creating Solution Cells <#creating-solution-cells>`_
* `Creating Tests <#creating-tests>`_

.. _cli-tools:

-------------
CLI Tools
-------------

-------------
``ds -begin``
-------------
When this command is run the following things happen:

* A ``data/`` folder is added to the current working directory
* A ``.solution_files`` subdirectory is added to the current working directory
* A ``curriculum.ipynb`` file is added to the current working directory
  
   * This notebook contains instructions for creating solution tags. See `Creating Solution Cells <#creating-solution-cells>`_.
   * All curriculum content needs to be created in this file in order to use ``ds -create``.


-------------
``ds -create``
-------------
When this command is run the following things happen:

- An ``index.ipynb`` file is added to the current working directory containing all "student facing" content within the ``curriculum.ipynb`` file
- An ``index.ipynb`` file is added to the ``.solution_files`` subdirectory containing all solution content in the ``curriculum.ipynb`` file.
- The ``curriculum.ipynb`` file is deleted
  
   - To make future edits to this project, the curriculum notebook must be generated using `ds -edit`.


-------------
``ds -edit``
-------------
When this command is run the following things happen:

* The metadata inside the lesson and solution notebooks is used to recompile the ``curriculum.ipynb`` notebook.

Once the curriculum notebook is compiled, edits to the lesson can be made inside ``curriculum.ipynb``.
Once edits are complete, run ``ds -create`` to hide the solutions inside a hidden folder.


-------------
``ds -share <Github notebook url>``
-------------

* This command accepts any link that points to a public notebook on github. When this command is run, a link is copied to your clipboard that points to the notebook on illumidesk.
* This command can be used to create `url module items in canvas <https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-add-an-external-URL-as-a-module-item/ta-p/967>`_.

-------------------------------------------------------

.. _creating-a-lesson:

Creating A Lesson
==================

**The overall proccess looks like this**

1. Create project folder
2. ``cd`` into the the project folder
3. Run ``ds -begin``
4. Open the ``curriculum.ipynb`` jupyter notebook
5. Create lesson using `solution tags <#creating-solution-cells>`_ 
6. Save the curriculum notebook
7. run ``ds -create``
8. Push repository to github
9. Copy link to the top level ``index.ipynb`` file on github.
10. run ``-ds share <github link>
11. Share link with students. 

**To make new edits to a lesson after running ``ds -create``**

1. run ``ds -edit``
2. Open the ``curriculum.ipynb`` notebook
3. Make edits in curriculum notebook
4. Save notebook
5. run ``ds -create``

Lesson Structure
==================

This toolkit uses the following directory structure for all lessons::

   lesson-directory 
         |
         index.ipynb
         curriculum.ipynb
         data
            |
            lesson_data.csv
         .solution_files
            |
            index.ipynb
            .test_obj
               |
               pickled_test.pkl 

* The top level ``index.ipynb`` file contains all student facing materials.
* The top level ``curriculum.ipynb` file is where all curriculum materials are created.
* The `data/` folder is not required, but tends to be best practice for most data science projects.
* The ``.solution_files`` hidden folder stores the solution content.
* The ``.solution_files/index.ipynb`` file is the notebook containing all solution code and markdown.
* The ``.test_obj`` folder contains all pickled test objects. See `Creating Tests <#creating-tests>`_


Creating Solution Cells
=======================

What ``ds -create`` is used, all solution cells are removed from the top level ``index.ipynb`` file 
and moved to the ``index.ipynb`` file in the ``.solution_files`` hidden folder. 

Solution cells can be created for both code and Markdown cells in Jupyter Notebooks.

**To create a solution Markdown cell**

Place ``==SOLUTION==`` at the top of a Markdown cell. This tag should have its own line.

**To create a solution code cell**

Place ``#__SOLUTION__`` at the top of the code cell. This tag should have its own line.

.. _test-code:

Creating Tests
==============

`dscreate` offers a couple options for adding tests to your curriculum materials.

NOTE: All tests are created and run using the `Tests` class within the `tests` subdirectory.::

         from dscreate.tests import Tests
         tests = Tests()

------------------------         
Writing Test Functions
------------------------

Below, is an example of a test for a simple problem. In this scenario a student is
tasked with generating the list ``[1,2,3]``. 

::

         #__SOLUTION__

         def test_function(student_answer):
            if student_answer == [1,2,3]:
               return True


         tests.save(test_function, 'first_test')

**Running a test**::

         student_solution = [1,2,2]

         tests.run('first_test', student_solution)
         tests.run('first_test', [1,2,3])

         >>>first_test: ❌
         >>>first_test: ✅

**Test function can use multiple arguments**::

         #__SOLUTION__
         def multiple_arg_test(arg1, arg2, arg3, arg4):
            if arg1 != [1,2,3]:
               return False
            elif arg2 != [3,2,1]:
               return False
            elif arg3 != 'hello world':
               return False
            elif arg4 != 51:
               return False
            else:
               return True
            
         tests.save(multiple_arg_test, 'multiple_arguments')

**Running a multiple argument test**::

         student_answer = [1,2,3], [3,2,1], 'hello world', 51
         tests.run('multiple_arguments', *student_answer)

         student_answer = [1,2,3], [3,2,1], 'hello flatiron', 51
         tests.run('multiple_arguments', *student_answer)

         >>>multiple_arguments: ✅
         >>>multiple_arguments: ❌

**If you would like to output the result of the test instead of ✅ or ❌, you can set assertion=False**::

         #__SOLUTION__
         def output_test(function):
            def solution(a,b):
               return a+b
            
            student = function(1,2)
            answer = solution(1,2)
            if student != answer:
               return f"Your function returned {student}, but should return {answer}!"
            else:
               return f'Your function returned the correct answer for 1 + 2!'
            

         tests.save(output_test, 'output_test', assertion=False)
   
**Running a test that returns the output of the test function**::

      def student_answer_wrong(a,b):
         return a-b

      def student_answer_correct(a,b):
         return a+b

      tests.run('output_test', student_answer_wrong)
      tests.run('output_test', student_answer_correct)

      >>>output_test: Your function returned -1, but should return 3!
      >>>output_test: Your function returned the correct answer for 1 + 2!

---------------------       
Writing A Test Class
---------------------

If you have multiple tests you'd like to run, the easiest solution would be create a class like below

* *All test methods must begin with the word `test`*
* If you would like to return the output of a test, set the argument `output=True` for the test method.

**Below is an example of a test class for the following student task:**

   "In the cell below, create a class that has an attribute called "attribute" and a method called "method". 
   The method should return the number 5."



::

         #__SOLUTION__
         class ExampleTest:
            
            def __init__(self, student_answer):
               self.student_answer = student_answer()
               
            def test_for_attribute(self):
               if hasattr(self.student_answer, 'attribute'):
                     return True
               
            def test_method_output(self, output=True):
               try:
                     result = self.student_answer.method()
                     if result == 5:
                        return 'Your method correctly returned 5!'
                     else:
                        return f'Your method returned {result} when it should have returned 5!'
               except:
                     return 'Your method threw an error.'
                     
                     
         tests.save(ExampleTest, 'Class_Example')


**Running the test class**::

         class StudentSolutionCorrect:
            
            def __init__(self):
               self.attribute = True
               
            def method(self):
               return 5
            
         tests.run('Class_Example', StudentSolutionCorrect)

         >>>test_for_attribute: ✅
         >>>test_method_output: Your method correctly returned 5!

::

         class StudentSolutionWrong:
            
            def method(self):
               return 3

         tests.run('Class_Example', StudentSolutionWrong)

         >>>test_for_attribute: ❌
         >>>test_method_output: Your method returned 3 when it should have returned 5!
