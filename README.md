# product-qrcode
qrcode generator for products with dynamic content.

## Preparation

Prepare a list of txt files which need to generated as qrcode with name format `{index}_{count}.txt`.

```
|--1_10.txt
|--2_100.txt
```


## Execution

Run below command with python3.

```
python qrcode.py
```

## Result

1. A base directory will be created with name pattrn `{date}_{time}`.
2. A sub directory with source file name under base directory.
3. Qrcode with svg extention will be saved in sub directory.
4. pdf file for each source file will be stored under the base directory with name pattern `qrcode{index}.pdf`.

```
|--{date}_{time}
    |--{index}_{count}
        |--qrcode_{qrcode_index}.svg
        ...
    |--qrcode{index}.pdf
```