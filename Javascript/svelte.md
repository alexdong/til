## Events

* I like how the event can pass data back up the rendering stack. In React, we
have to pass it down through the `Props`. We can also use `createContext` but
it's not for passing information back up. 
* Event forwarding feels like unnecessary though but maybe it's just an
attempt to make data going back up more explicit.
* Value binding is so much better `<input bind:value={name} />`. And the type
conversion that comes with it like `<input type=number .../>` is super handy.
* `bind:checked` and `bind:group` kick React's butt.
* I'm really enjoying the intentional effort to minimise boilerplates. For
example `<textarea bind:value></textarea>` will automatically bind to a variable
called `value`.

