function print() {
    var value = $("#value").val();
    var bigint = BigInteger(value);
    var y, yy, xx = 0;
    var context = $("#canvas")[0].getContext('2d');
    context.fillStyle = "#000000";
    context.fillRect(0, 0, 106 * 4, 17 * 4);
    for (x = 105; x >= 0; x--) {
        yy = 0;
        y = bigint;
        for (v = 0; v <= 16; v++) {
            if (BigInteger.remainder(BigInteger.divide(BigInteger.divide(y, 17), BigInteger.pow(2, (17 * x) + BigInteger.remainder(y, 17))), 2) > 0.5) {
                context.fillStyle = "#ffffff";
                context.fillRect(xx, yy, 3, 3);
            }
            y = BigInteger.add(y, 1);
            yy += 4;
        }
        xx += 4;
    }
    var hash = CryptoJS.SHA1(CryptoJS.SHA1(value).toString()).toString();
    if (hash == '75c2be0c0c721ceb2ae44978b093b3b7f493638f') {
        window.location.href = "flag_" + CryptoJS.SHA1(value).toString() + '.html';
    }
}

y_div = BigInteger.divide(y, 17)
y_r = BigInteger.remainder(y, 17)
x_pow = BigInteger.pow(2, (17 * x) + y_r)
BigInteger.remainder(BigInteger.divide(y_div, x_pow), 2)