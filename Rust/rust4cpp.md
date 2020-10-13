Book notes from `Rust for C++ programmers`.

## Hello world

* `cargo build` and `cargo run`, like `make && make install`
* `println!("Hello")`, the `!` means `println` is a macro.
* `return` is optional. It can be used for an early return. If the last
statement in a function is not finished with a `;`, then it is the return value. 
* Use `{?}` in `println!` to print detailed debug info.

## Control flow

* `{}` in rust is mandatory but the `()` around the conditions are not.
* `if` is a statement so we can write `let x = if ...`.
* There is no `?:` in rust because of the above point. 
* `for .. in` works on `iterator`.
  * `for n in 0..101` or `for n in 0..=100` are the same.
  * `for n in numbers.iter()` where `numbers: Vec<i32>`
  * `for (i, n) in numbers.iter().enumerate` works just like Python.
* 3 type of iterators
  * `into_iter` is the default behaviour. It allows only one pass.
  * `iter` allows multiple read-only passes.
  * `iter_mut` borrows each element of the collection for in place modification.
* `match =>` is like `switch` with pattern matching capability. 
  * Use `_` and `{}` to ignore one possibility. 
  * Use `variable` as a walrus assignment like in Python 3.8.
  * We can also use `if` statement as a condition like `match var { y if y < 100`  
