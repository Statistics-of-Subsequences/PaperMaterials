# Supporting document for Binary-RAMOnly.cpp
To set your desired parameters, see the USER PARAMETERS section at the top of Binary-RAMOnly.cpp.

**NOTE: Binary-RAMOnly.cpp consumes 2^(2*length -1) * 4 * 2 = 4^(length+1) bytes of memory. If you do not have enough RAM for the length parameter you set, it (being the program or possibly your entire system) will probably crash/run extremely slowly. Always verify you have enough RAM before running!**


## Optimizations
Binary-RAMOnly.cpp does not directly follow the explanation in the paper. Namely, a few optimizations are made so that it runs faster and uses less memory. Note that Binary-RAMOnly.cpp does *not* implement any form of external memory reading/writing, the algorithm which does so is in Binary-ExtnMem.cpp. 

#### Local Maximums and Computation Reuse
Most prominently, $L_{01}$ and $L_{10}$ have been combined into one loop. This way, elementwise maximums can be done locally instead of separately in F, which saves time (both due to locality of computation, and also because it means a separate loop performing a max over $2^{(length-2)}$ elements is not needed). So, when computing an element $s_1$ in $L_{01}$'s range, we also compute an element $s_3$ in $L_{10}$'s range to perform the max with.  
Additionally, given a string in $L_{01}$'s range (here, $s_1$), we make the observation that the accesses for that element are related to the accesses for an element in $L_{10}$'s range ($s_2$) and use that fact to reuse some computations. Of course, since we computed $s_3$, we can similarly reuse computations for $s_3$ to help calculate another element in $L_{01}$'s range ($s_4$). In fact, $s_4$ is exactly the element that needs to be `max`'d with $s_2$.  
In total, this means that instead of computing just one value at once, we compute four values: one for $L_{01}$ ($s_1$), one for $L_{10}$ ($s_3$) to perform a `max` on $s_1$ with, one value ($s_2$) in $L_{10}$ which we reuse some computations from $s_1$ for, and one value in $L_{01}$ ($s_4$) which we reuse some computations from $s_3$ for. Then, $s_1$ is `max`'d with $s_3$ and $s_2$ is `max`'d with $s_4$, and we are left with two values. See the comments at lines 92-120 of Binary-RAMOnly.cpp for a detailed explanation of the calculations performed.

#### Symmetry of $L_{00}$
It is also noted how, for $L_{00}$, we can use the symmetric transformations described in Section 3.3 to our advantage. Since $L_{00}$ iterates only from $[0, ..., 2^{2ℓ−2})$, the first bit of a and b will always be 0. Thus, for a given x, the procedure always accesses the values at 4x, 4x + 1, 4x + 2, and 4x + 3. For $x ≥ 2^{2ℓ−3}$, it will access pairs greater than or equal to 2$^{2ℓ−1}$, which fall outside the vector.  
However, instead of straightforwardly transforming the pairs back to their symmetric position within the vector using Equation 3.10, we can instead observe that all that occurs when doing this transformation for the second half of $L_{00}$ is that the elements it accesses are reversed. Thus, the sequence of values $L_{00}$ outputs is symmetric about its center (self-symmetric). So, instead of doing this symmetric transformation with Equation 3.10 and recomputing the value, we can instead just set $v[2^{2ℓ−2}-1 - x] = v[x]$. (Indeed, we can avoid even setting these values at all and instead implicitly assume that $v[2^{2ℓ−2}-1 - x] = v[x]$ whenever we access values from the second quarter of $v$, and thus we need not even store the second quarter of $v$, but for the sake of notational simplicity we act as if all values in $v$ have been set.)


#### Adjusted Bound Calculation For Two Vectors
Additionally, as mentioned by Lueker, instead of storing three vectors and performing a recurrence on them, we need only store two. The bound calculation also gets adjusted because of this.
Instead of calculating an $R$ and $E$, in the binary case, we need only calculate the minimum elementwise change between the two vectors in the recurrence (i.e., min_change is defined like $R$ in the Binary Feasible Triplet Algorithm, except `min` is performed instead of `max`). The bound is then calculated as (2*min_change)/(1+min_change), as described by Lueker.

#### Skipping Bound Calculation and Early Stopping 
Empirically, we observe that the value of $R-E$ (or min_change) at iteration $n$ is less than or equal to the value of $R-E$ (or min_change) at iteration $m$, for $n < m$. Thus, we need not calculate $R$, $E$, or **$W$** (or min_change) every iteration. Instead, we calculate it every X iterations (a user parameter), and halt the process early if the change from its previous value does not exceed a certain threshold (and the value is not 0). This early stopping detects the convergence of $v_{d+n}$ to $v_{n} + dr$. In combination, implementing these two adjustments reduces both the computation per iteration and the total number of iterations, resulting in a noticeable speedup.

