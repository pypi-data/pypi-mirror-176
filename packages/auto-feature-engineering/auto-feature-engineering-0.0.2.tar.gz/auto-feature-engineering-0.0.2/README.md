# Intro

This is a package for automatically feature engineering. 

Suitable for tabular numerical data and the classification modelling.



## Install

```shell
pip install auto-feature-engineering
```



## Usage

```python
from autofe import autofe

x_train, x_test, y_train, y_test, feature_cols = load_data()

afe = autofe.AutoFE('primary_key', feature_cols)

afe.fit(x_train, y_train)

x_train = afe.transform(x_train)
x_test = afe.transform(x_test)

finaldf = afe.generator(x_train, x_test, y_train, y_test)
```



## Examples

To see how the demo for running the package, see the [demo](tests/demo.py).



## Contributing

[@XinlinWang](https://github.com/LeylaWong)



## License

[MIT](LICENSE) © Xinlin Wang



