
The singlet transition is modeled as a step function convolved with a Gaussian temporal response:

$$
f_1(t)
=
f_\mathrm{after}
+
\frac{\Delta f}{2}
\operatorname{erfc}
\left(
\frac{t-t_0}{\sqrt{2}\sigma_t}
\right)
$$

In the code:

```python
def model(time, population_after, population_drop, t0, sigma_time):
    return population_after + 0.5 * population_drop * erfc(
        (time - t0) / (np.sqrt(2.0) * sigma_time)
    )
```

Parameters:

- `population_after`: Singlet population after the transition
- `population_drop`: Difference between the initial and final singlet population
- `t0`: Time at which the population has fallen by 50%
- `sigma_time`: Standard deviation of the Gaussian time response

For $t \ll t_0$:

$$
f_1(t)\approx f_\mathrm{after}+\Delta f
$$

For $t \gg t_0$:

$$
f_1(t)\approx f_\mathrm{after}
$$

The corresponding temporal width is:

$$
\mathrm{FWHM}
=
2\sqrt{2\ln 2}\,\sigma_t.
$$

So this model assumes an **instantaneous population change**, blurred by the Gaussian laser/cross-correlation response. 
