# Monoids




[Copy-pasted from Haskell]
[@TODO: Summarize]

class Monoid a where Source

> The class of monoids (types with an associative binary operation that has an identity). 

Laws
--------
In Haskell terms

```haskell
mappend mempty x = x
mappend x mempty = x
mappend x (mappend y z) = mappend (mappend x y) z
mconcat = foldr mappend mempty
```

The method names refer to the monoid of lists under concatenation, but there are many other instances.

Some types can be viewed as a monoid in more than one way, e.g. both addition and multiplication on numbers. In such cases we often define newtypes and make those instances of Monoid, e.g. Sum and Product.

Minimal complete definition
mempty, mappend

Methods
mempty :: a Source

Identity of mappend

mappend :: a -> a -> a Source

An associative operation

mconcat :: [a] -> a Source

Fold a list using the monoid. For most types, the default definition for mconcat will be used, but the function is included in the class definition so that an optimized version can be provided for specific types.



class Monoid a where
        mempty  :: a
        -- ^ Identity of 'mappend'
        mappend :: a -> a -> a
        -- ^ An associative operation
        mconcat :: [a] -> a

        -- ^ Fold a list using the monoid.
        -- For most types, the default definition for 'mconcat' will be
        -- used, but the function is included in the class definition so
        -- that an optimized version can be provided for specific types.

        mconcat = foldr mappend mempty





ASIDE: Annoyingly, the Prelude definition of `foldr` gets involved:
    -- | Map each element of the structure to a monoid,
    -- and combine the results.
    foldMap :: Monoid m => (a -> m) -> t a -> m
    foldMap f = foldr (mappend . f) mempty

    -- | Right-associative fold of a structure.
    --
    -- @'foldr' f z = 'Prelude.foldr' f z . 'toList'@
    foldr :: (a -> b -> b) -> b -> t a -> b
    foldr f z t = appEndo (foldMap (Endo #. f) t) z

And this requires `appEndo`/`Endo`, and understanding that takes us down a rabbit hole at least as complicated

All I can really see from this, is that it is easiest to involve some list function ('for' loop)



class Monoid a where
        mempty  :: a
        -- ^ Identity of 'mappend'
        mappend :: a -> a -> a
        -- ^ An associative operation
        mconcat :: [a] -> a

        -- ^ Fold a list using the monoid.
        -- For most types, the default definition for 'mconcat' will be
        -- used, but the function is included in the class definition so
        -- that an optimized version can be provided for specific types.

        mconcat = foldr mappend mempty

instance Monoid [a] where
        {-# INLINE mempty #-}
        mempty  = []
        {-# INLINE mappend #-}
        mappend = (++)
        {-# INLINE mconcat #-}
        mconcat xss = [x | xs <- xss, x <- xs]
