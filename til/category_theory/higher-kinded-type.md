Higher Kinded Type
==========================
What is a higher kinded type?
* Higher kinded types are types which take other types and construct a new type
* A higher kinded type is a concept that reifies a type constructor as an actual type
* Higher kinded type == type constructor which takes type constructor as a type parameter?

In other peoples words:
-------------
In the words of (Roger Qiu)[https://gist.github.com/CMCDragonkai/a5638f50c87d49f815b8]:
> A type constructor can be thought of in these analogies:
> * like a function in the type universe
> * as a type with a "hole" in it
> * as a container containing type(s)
> * as a generic type, parameterised over other types
> * as an endofunctor in the category of types



Take from wikipedia, on (Kinds in the context of type theory)[https://en.wikipedia.org/wiki/Kind_(type_theory)]:
> ... a kind is the type of a type constructor or, less commonly, the type of a higher-order type operator. 
> ... A kind is sometimes confusingly described as the "type of a (data) type", but it is actually more of an arity specifier. Syntactically, it is natural to consider polymorphic types to be type constructors, thus non-polymorphic types to be nullary type constructors. But all nullary constructors, thus all monomorphic types, have the same, simplest kind; namely *.


Why do we care?
--------------------
[Generic programming](https://en.wikipedia.org/wiki/Generic_programming), and the programming techniques derived from category-theory (such as functors, monads, and arrows), make extensive use of higher-kinded structures. Although the types of these higher-kinded structures are well-defined and statically inferrable, expressing them in classic type-systems will be either difficult or impossible. Classic type-systems in this context are those which use name-based typing, properly called [nominal-typing](https://en.wikipedia.org/wiki/Nominal_type_system), such as C++ without templates, or  C, C#, and Java.

Specifically, higher-kinded types are a prerequisite for the ability to do (static) type-analysis on functorial and monadic structures. A limited form of higher-kinded types is available in most major languages, in the form of generic-classes (C#) or generic-types (Java). However, this form of generics is incapable of expressing the function-transforming aspect of functors, and consquently cannot express monads either.
