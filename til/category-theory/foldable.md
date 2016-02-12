# Foldable

The category of things which can meaningfully be subject to a 'reduce' or 'fold' style operation.

In Haskell, this is a shortened summary of what it looks like:

```haskell
class Foldable t where
    {-# MINIMAL foldMap | foldr #-}

    -- | Right-associative fold of a structure.
    --
    -- @'foldr' f z = 'Prelude.foldr' f z . 'toList'@
    -- Obeys Law: foldr f z = foldr f z . toList
    foldr :: (a -> b -> b) -> b -> t a -> b
    foldr f z t = appEndo (foldMap (Endo #. f) t) z

    -- | Map each element of the structure to a monoid,
    -- and combine the results.
    foldMap :: Monoid m => (a -> m) -> t a -> m
    foldMap f = foldr (mappend . f) mempty

    -- | Combine the elements of a structure using a monoid.
    fold :: Monoid m => t m -> m
    fold = foldMap id

    -- | List of elements of a structure, from left to right.
    toList :: t a -> [a]
    {-# INLINE toList #-}
    toList t = build (\ c n -> foldr c n t)

    -- | Test whether the structure is empty. The default implementation is
    -- optimized for structures that are similar to cons-lists, because there
    -- is no general way to do better.
    null :: t a -> Bool
    null = foldr (\_ _ -> False) True

    -- | Returns the size/length of a finite structure as an 'Int'.  The
    -- default implementation is optimized for structures that are similar to
    -- cons-lists, because there is no general way to do better.
    length :: t a -> Int
    length = foldl' (\c _ -> c+1) 0

    -- | Does the element occur in the structure?
    elem :: Eq a => a -> t a -> Bool
    elem = any . (==)
```

An example implementations (instances) for a tree data structure:
```haskell
-- Using foldMap
instance Foldable Tree where
   foldMap f Empty = mempty
   foldMap f (Leaf x) = f x
   foldMap f (Node l k r) = foldMap f l `mappend` f k `mappend` foldMap f r

-- Using foldR
instance Foldable Tree where
   foldr f z Empty = z
   foldr f z (Leaf x) = f x z
   foldr f z (Node l k r) = foldr f (f k (foldr f z r)) l
```

Example for Maybe:
```haskell
instance Foldable Maybe where
    foldr _ z Nothing = z
    foldr f z (Just x) = f x z

    foldl _ z Nothing = z
    foldl f z (Just x) = f z x
```

Example for Either:
```haskell
instance Foldable (Either a) where
    foldMap _ (Left _) = mempty
    foldMap f (Right y) = f y

    foldr _ z (Left _) = z
    foldr f z (Right y) = f y z

    length (Left _)  = 0
    length (Right _) = 1

    null             = isLeft
```


An example for List
```haskell
foldr            :: (a -> b -> b) -> b -> [a] -> b
-- foldr _ z []     =  z
-- foldr f z (x:xs) =  f x (foldr f z xs)
```
```

Specialized folds:
```haskell
concat :: Foldable t => t [a] -> [a] Source
```
The concatenation of all the elements of a container of lists.
```haskell
concatMap :: Foldable t => (a -> [b]) -> t a -> [b] Source
```
Map a function over all the elements of a container and concatenate the resulting lists.
```haskell
and :: Foldable t => t Bool -> Bool Source
```
and returns the conjunction of a container of Bools. For the result to be True, the container must be finite; False, however, results from a False value finitely far from the left end.
```haskell
or :: Foldable t => t Bool -> Bool Source
```
or returns the disjunction of a container of Bools. For the result to be False, the container must be finite; True, however, results from a True value finitely far from the left end.
```haskell
any :: Foldable t => (a -> Bool) -> t a -> Bool Source
```
Determines whether any element of the structure satisfies the predicate.
```haskell
all :: Foldable t => (a -> Bool) -> t a -> Bool Source
```
Determines whether all elements of the structure satisfy the predicate.
```haskell
maximumBy :: Foldable t => (a -> a -> Ordering) -> t a -> a Source
```
The largest element of a non-empty structure with respect to the given comparison function.
```haskell
minimumBy :: Foldable t => (a -> a -> Ordering) -> t a -> a Source
```
The least element of a non-empty structure with respect to the given comparison function.

Searches
```haskell
notElem :: (Foldable t, Eq a) => a -> t a -> Bool infix 4 Source
```
notElem is the negation of elem.
```haskell
find :: Foldable t => (a -> Bool) -> t a -> Maybe a Source
```
The find function takes a predicate and a structure and returns the leftmost element of the structure matching the predicate, or Nothing if there is no such element.




An example of this implemented in Python is here [foldable.py](#foldable.py)

