_ = function (e) {
    m = function (e, t, n) {
        g = function () {
            return ["i", "/", "x", "1", "X", "g", "U", "0", "z", "7", "k", "8", "N", "+", "l", "C", "p", "O", "n", "P", "r", "v", "6", "\\", "q", "u", "2", "G", "j", "9", "H", "R", "c", "w", "T", "Y", "Z", "4", "b", "f", "S", "J", "B", "h", "a", "W", "s", "t", "A", "e", "o", "M", "I", "E", "Q", "5", "m", "D", "d", "V", "F", "L", "K", "y"]
        }
        b = function () {
            return "3"
        }
        var i, r, o, a = g(), s = b(), l = [];
        if (1 == n)
            i = e[t],
                r = 0,
                o = 0,
                l.push(a[i >>> 2 & 63]),
                l.push(a[(i << 4 & 48) + (r >>> 4 & 15)]),
                l.push(s),
                l.push(s);
        else if (2 == n)
            i = e[t],
                r = e[t + 1],
                o = 0,
                l.push(a[i >>> 2 & 63]),
                l.push(a[(i << 4 & 48) + (r >>> 4 & 15)]),
                l.push(a[(r << 2 & 60) + (o >>> 6 & 3)]),
                l.push(s);
        else {
            if (3 != n)
                throw new Error("1010");
            i = e[t],
                r = e[t + 1],
                o = e[t + 2],
                l.push(a[i >>> 2 & 63]),
                l.push(a[(i << 4 & 48) + (r >>> 4 & 15)]),
                l.push(a[(r << 2 & 60) + (o >>> 6 & 3)]),
                l.push(a[63 & o])
        }
        return l.join("")
    }

    if (null == e || void 0 == e)
        return null;
    if (0 == e.length)
        return "";
    var t = 3;

    for (var n = [], i = 0; i < e.length;) {
        if (!(i + t <= e.length)) {
            n.push(m(e, i, e.length - i));
            break
        }
        n.push(m(e, i, t)),
            i += t
    }
    return n.join("")

}

// 小段轨迹加密
function n(e, t) {
    function n(e, t) {
        return e.charCodeAt(Math.floor(t % e.length))
    }

    function i(e, t) {
        return t.split("").map(function (t, i) {
            return t.charCodeAt(0) ^ n(e, i)
        })
    }

    return t = i(e, t),
        _(t)
}


function encryptionTrajectory(token, step) {
    return n(token, step)
}