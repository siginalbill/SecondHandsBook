function Book_Details() {
    $("#button_buy").click(function () {
        postdata["tradebrief"] = $("#trade_remark").val();
        postdata["checkcode"] = $("#check_str").val();
        //            console.log(postdata);
        $.post("/book/submit_trade/", postdata, function (data) {
            if (data["error"]) {
                rsp = "购买失败：" + data["error"];
                alert(rsp);
            }
            else {
                rsp = [
                    "购买成功！\n"
                    , "您购买的商品为："
                    , data["bookname"]
                    , "\r成交价格："
                    , data["booksell"]
                    , "\r交易时间："
                    , data["tradetime"]
                    , "\n卖家："
                    , data["sellname"]
                    , "\r卖家微信号："
                    , data["wechat"]
                    , "\r卖家qq号："
                    , data["tencentqq"]
                    , "\r卖家其他联系方式："
                    , data["callothers"]
                    , "\n交易备注："
                    , data["tradebrief"]

                ].join("");
                alert(rsp);
            }
        });
    });
    // 点击一次,更改图片内容,
    $("#check_code").click(function () {
        $(this).attr("src", "/check_code/?" + String(Math.random()));
        console.log("test");
    });
}

function Book_Sale() {
    function CheckNull() {
        var num = 1;
        $("input[type$='text']").each(function (n) {
            if ($(this).attr("name") == "wechat") {
                if ($(this).val() == "") { }
                else { num--; }
                console.log(num);
            }
            else if ($(this).attr("name") == "tencentqq") {
                if ($(this).val() == "") { }
                else { num--; }
                console.log(num);
            }
            else if ($(this).attr("name") == "callothers") {
                if ($(this).val() == "") { }
                else { num--; }
                console.log(num);
            }
            else if ($(this).val() == "") {
                num++;
                console.log(num);
            }
        });
        if (num > 0) {
            return true;
        }
        else {
            return false;
        }
    }
    var CheckSubmitFlg = false;
    function CheckSubmit() {
        if (CheckSubmitFlg == true) {
            return true;
        }
        CheckSubmitFlg = true;
        return false;
    }
    function CheckSessionFlg() {
        book_p = $("#bookname").val();
        if (book_p == $.session.get('book_session')) {
            return true;
        }
        else {
            $.session.set('book_session', book_p);
            return false;
        }
    }
    $("document").ready(
        $("form").submit(function (e) {
            if (CheckNull()) {
                e.preventDefault();
                $("#ErrorMessage").text("不能有空项！");
            }
                //            if (CheckSubmit()) {
                //                e.preventDefault();
                //                $("#ErrorMessage").text("不要重复提交！");
                //            }
            else if (CheckSessionFlg()) {
                e.preventDefault();
                $("#ErrorMessage").text("不要重复提交同一书目！");
            }
        })
    );
}

function Login() {
    $("#regist").click(function () {
        window.location.href = "/regist/"
    });
    $("#tourist").click(function () {
        window.location.href = "/tourist/"
    });
    // 点击一次,更改图片内容,
    $("#check_code").click(function () {
        $(this).attr("src", "/check_code/?" + String(Math.random()));
        console.log("test");
    });
}

function Main() {
    var page = 0;
    function checkpage() {
        $("#pagedown").click(function () {
            if (page > 0) {
                --page;
                $("#new_data").trigger("click");
            }
        });
        $("#pageup").click(function () {
            ++page;
            $("#new_data").trigger("click");
        });
    }
    $("document").ready(function () {
        checkpage();
        function newest_data() {
            $.getJSON('/book/newest_data/', { "page": page }, function (ret) {
                var list_str = ''
                list_str = [
                    '<tr>'
                    , '<td>书籍</td>'
                    , '<td>名称</td>'
                    , '<td>作者</td>'
                    , '<td>出版社</td>'
                    , '<td>详细信息</td>'
                    , '<td>售价</td>'
                    , '<td>原价</td>'
                    , '</tr>'
                ].join("\n");
                var bookimg
                var bookname
                var bookauthor
                var bookpublish
                var bookbrief
                var bookid
                var booksell
                var bookprice
                $.each(ret, function (i, item) {
                    $.each(item, function (key, value) {
                        if (key == "bookimg") {
                            if (value == "") {
                                bookimg = [
                                 '<td><img src="/static/img/'
                                 , 'normal.jpg'
                                 , '"style="height:50px; width:50px;"/></td>'
                                ].join("");
                            }
                            else {
                                bookimg = [
                                 '<td><img src="/media/'
                                 , value
                                 , '"style="height:50px; width:50px;"/></td>'
                                ].join("");
                            }
                        }
                        else if (key == "bookname") {
                            bookname = '<td>' + value + '</td>';
                        }
                        else if (key == "bookauthor") {
                            bookauthor = '<td>' + value + '</td>';
                        }
                        else if (key == "bookpublish") {
                            bookpublish = '<td>' + value + '</td>';
                        }
                        else if (key == "bookbrief") {
                            bookbrief = '<td>' + value + '</td>';
                        }
                        else if (key == 'bookid') {
                            bookid = value;
                        }
                        else if (key == 'booksell') {
                            booksell = '<td><strong>' + value + '</strong></td>';
                        }
                        else if (key == 'bookprice') {
                            bookprice = '<td>' + value + '</td>';
                        }
                    })
                    list_str = list_str + [
                        '<tr class = "book_list" bookid = "'
                        , bookid
                        , '">'
                        , bookimg
                        , bookname
                        , bookauthor
                        , bookpublish
                        , bookbrief
                        , booksell
                        , bookprice
                        , '</tr>'
                    ].join('');
                });
                $("#show_data").html(list_str);
            });
        }
        $("#new_data").click(function () {
            newest_data();
        });
        $("#show_data").on("click", ".book_list", function () {
            window.open( "/book/details?bookid=" + $(this).attr("bookid"));
        });
        $("#submit_search").click(function () {
            $.getJSON('/book/search_data/', { "searchstr": $("#search_str").val() }, function (ret) {
                var list_str = ''
                list_str = [
                    '<tr>'
                    , '<td>书籍</td>'
                    , '<td>名称</td>'
                    , '<td>作者</td>'
                    , '<td>出版社</td>'
                    , '<td>详细信息</td>'
                    , '<td>售价</td>'
                    , '<td>原价</td>'
                    , '</tr>'
                ].join("\n");
                var bookimg
                var bookname
                var bookauthor
                var bookpublish
                var bookbrief
                var bookid
                var booksell
                var bookprice
                $.each(ret, function (i, item) {
                    $.each(item, function (key, value) {
                        if (key == "bookimg") {
                            if (value == "") {
                                bookimg = [
                                 '<td><img src="/static/img/'
                                 , 'normal.jpg'
                                 , '"style="height:50px; width:50px;"/></td>'
                                ].join("");
                            }
                            else {
                                bookimg = [
                                 '<td><img src="/media/'
                                 , value
                                 , '"style="height:50px; width:50px;"/></td>'
                                ].join("");
                            }
                        }
                        else if (key == "bookname") {
                            bookname = '<td>' + value + '</td>';
                        }
                        else if (key == "bookauthor") {
                            bookauthor = '<td>' + value + '</td>';
                        }
                        else if (key == "bookpublish") {
                            bookpublish = '<td>' + value + '</td>';
                        }
                        else if (key == "bookbrief") {
                            bookbrief = '<td>' + value + '</td>';
                        }
                        else if (key == 'bookid') {
                            bookid = value;
                        }
                        else if (key == 'booksell') {
                            booksell = '<td><strong>' + value + '</strong></td>';
                        }
                        else if (key == 'bookprice') {
                            bookprice = '<td>' + value + '</td>';
                        }
                    })
                    list_str = list_str + [
                        '<tr class = "book_list" bookid = "'
                        , bookid
                        , '">'
                        , bookimg
                        , bookname
                        , bookauthor
                        , bookpublish
                        , bookbrief
                        , booksell
                        , bookprice
                        , '</tr>'
                    ].join('');
                });
                $("#show_data").html(list_str);
            });
        });
        newest_data();
    });
}

function MyAccount() {
    function bookbuyinit() {
        $.getJSON('/book/account_bookbuy/', function (ret) {
            console.log(ret);
            var list_str = ''
            var title_str = [
                '<tr>'
                , '<td>书籍</td>'
                , '<td>名称</td>'
                , '<td>购买价格</td>'
                , '<td>订单状态</td>'
                , '<td>卖家</td>'
                , '<td>卖家联系方式(微信/qq/其他)</td>'
                , '<td>交易信息</td>'
                , '<td>下单时间</td>'
                , '<td>操作</td>'
                , '</tr>'
            ].join("\n");
            var bookimg
            var bookname
            var bookid
            var booksell
            var status
            var contact
            var sellerername
            var tradebrief
            var tradetime
            var operations
            $.each(ret, function (i, item) {
                if (item["bookimg"] == "") {
                    bookimg = [
                             '<td><img src="/static/img/'
                             , 'normal.jpg'
                             , '"style="height:50px; width:50px;"/></td>'
                    ].join("");
                }
                if (item["bookimg"] != "") {
                    bookimg = [
                            '<td><img src="/media/'
                            , item["bookimg"]
                            , '"style="height:50px; width:50px;"/></td>'
                    ].join("");
                }
                bookname = '<td>' + item["bookname"] + '</td>';
                bookid = item["bookid"];
                booksell = booksell = '<td>￥' + item["booksell"] + '</td>';
                if (item["status"] == 0) {
                    return true;
                }
                if (item["status"] == 1) {
                    status = '<td><strong>' + '等待完成交易' + '</strong></td>';
                    sellername = '<td>' + item["sellername"] + '</td>';
                    contact = '<td>' + [item["wechat"], item["tencentqq"], item["callothers"]].join("/") + '</td>';
                    tradebrief = '<td>' + item["tradebrief"] + '</td>';
                    trdadetime = '<td>' + item["tradetime"] + '</td>';
                    operations = '<td class="op"><a class="a_show" href="#" bookid = "' + bookid + '">查看</a>' + ' <a class="a2_show" href="/chat/chat/?recver_name=' + sellername + '">联系卖家</a>' + ' <a id="buy_cancel" bookid="' + bookid + '" href="#">取消订单</a></td>';
                }
                if (item["status"] == 2) {
                    status = '<td><strong>' + '完成交易' + '</strong></td>';
                    sellername = '<td>' + item["sellername"] + '</td>';
                    contact = '<td>' + [item["wechat"], item["tencentqq"], item["callothers"]].join("/") + '</td>';
                    tradebrief = '<td>' + item["tradebrief"] + '</td>';
                    trdadetime = '<td>' + item["tradetime"] + '</td>';
                    operations = '<td class="op"><a class="a_show" href="#" bookid = "' + bookid + '">查看</a>' + ' <a class="a2_show" href="/chat/chat/?recver_name=' + sellername + '">联系卖家</a>' + ' <a id="sell_already" bookid="' + bookid + '" href="#">已结束</a></td>';
                }

                list_str = [
                    '<tr class="book_item" id = "book_list_'
                    , item["status"]
                    , '" bookid = "'
                    , bookid
                    , '">'
                    , bookimg
                    , bookname
                    , booksell
                    , status
                    , sellername
                    , contact
                    , tradebrief
                    , trdadetime
                    , operations
                    , '</tr>'
                ].join('') + list_str;
            });
            $("#show_data").html(title_str + list_str);
        });
    }
    function bookbuy() {
        //////////////////////////view my goods///////////////////////////////////
        $("#account_bookbuy").click(function () {
            bookbuyinit();
        });
    }
    function booksell() {
        $("#account_booksell").click(function () {
            $.getJSON('/book/account_booksell/', function (ret) {
                var list_str = ''
                var title_str = [
                    '<tr>'
                    , '<td>书籍</td>'
                    , '<td>名称</td>'
                    , '<td>售价</td>'
                    , '<td>订单状态</td>'
                    , '<td>买家</td>'
                    , '<td>交易信息</td>'
                    , '<td>下单时间</td>'
                    , '<td>操作</td>'
                    , '</tr>'
                ].join("\n");
                var bookimg
                var bookname
                var bookid
                var booksell
                var status
                var buyername
                var tradebrief
                var tradetime
                var operations
                $.each(ret, function (i, item) {
                    if (item["bookimg"] == "") {
                        bookimg = [
                                 '<td><img src="/static/img/'
                                 , 'normal.jpg'
                                 , '"style="height:50px; width:50px;"/></td>'
                        ].join("");
                    }
                    if (item["bookimg"] != "") {
                        bookimg = [
                                '<td><img src="/media/'
                                , item["bookimg"]
                                , '"style="height:50px; width:50px;"/></td>'
                        ].join("");
                    }
                    bookname = '<td>' + item["bookname"] + '</td>';
                    bookid = item["bookid"];
                    booksell = booksell = '<td>￥' + item["booksell"] + '</td>';
                    if (item["status"] == 0) {
                        status = '<td><strong>' + '未售出' + '</strong></td>';
                        buyername = '<td>' + "无" + '</td>';
                        tradebrief = '<td>' + "无" + '</td>';
                        trdadetime = '<td>' + "无" + '</td>';
                        operations = '<td class="op"><a class="a_show" href="#" bookid = "' + bookid + '">查看</a>' + ' <a id="sell_delete" bookid="' + bookid + '" href="#">删除</a></td>';
                    }
                    if (item["status"] == 1) {
                        status = '<td><strong>' + '待确认' + '</strong></td>';
                        buyername = '<td>' + item["buyername"] + '</td>';
                        tradebrief = '<td>' + item["tradebrief"] + '</td>';
                        trdadetime = '<td>' + item["tradetime"] + '</td>';
                        operations = '<td class="op"><a class="a_show" href="#" bookid = "' + bookid + '">查看</a>' + ' <a class="a2_show" href="/chat/chat/?recver_name= ' + buyername + '">联系买家</a>' + ' <a id="sell_makesure" bookid="' + bookid + '" href="#">确认完成交易</a> <a id="sell_refuse" bookid="' + bookid + '" href="#">拒绝交易</a></td>';
                    }
                    if (item["status"] == 2) {
                        status = '<td><strong>' + '已售出' + '</strong></td>';
                        buyername = '<td>' + item["buyername"] + '</td>';
                        tradebrief = '<td>' + item["tradebrief"] + '</td>';
                        trdadetime = '<td>' + item["tradetime"] + '</td>';
                        operations = '<td class="op"><a class="a_show" href="#" bookid = "' + bookid + '">查看</a>' + ' <a class="a2_show" href="/chat/chat/?recver_name= ' + buyername + '">联系买家</a>' + ' <a id="sell_already" bookid="' + bookid + '" href="#">已结束</a></td>';
                    }

                    list_str = [
                        '<tr class="book_item" id = "book_list_'
                        , item["status"]
                        , '" bookid = "'
                        , bookid
                        , '">'
                        , bookimg
                        , bookname
                        , booksell
                        , status
                        , buyername
                        , tradebrief
                        , trdadetime
                        , operations
                        , '</tr>'
                    ].join('') + list_str;
                });
                $("#show_data").html(title_str + list_str);
            });
        });
    }    
    $("document").ready(function () {       
        bookbuyinit();
        bookbuy();
        booksell();
        $("#show_data").on("click", "#sell_refuse", function () {
            var postdata = {};
            postdata["method"] = "refuse"
            postdata["bookid"] = $(this).attr("bookid");
            var hides = this;
            $.post("/book/account_booksell/", postdata, function (data) {
                if (data["status"]) {
                    $(hides).hide();
                    $(hides).parent().children("#sell_makesure").hide();
                    alert("已拒绝交易请求，您的图书可以重新被预定");
                }
                else {
                    alert("请求失败");
                }
            });
        });
        $("#show_data").on("click", "#sell_delete", function () {
            var postdata = {};
            postdata["method"] = "delete"
            postdata["bookid"] = $(this).attr("bookid");
            var hides = this;
            $.post("/book/account_booksell/", postdata, function (data) {
                if (data["status"]) {
                    $(hides).hide();
                    $(hides).parent().children(".a_show").hide();
                    alert("已删除订单");
                }
                else {
                    alert("请求失败");
                }
            });
        });
        $("#show_data").on("click", ".a_show", function () {
            window.open("/book/details?bookid=" + $(this).attr("bookid"));
        });
        $("#show_data").on("click", "#buy_cancel", function () {
            var postdata = {};
            postdata["bookid"] = $(this).attr("bookid");
            var hides = this;
            //            console.log($(hides).parent());
            $.post("/book/account_bookbuy/", postdata, function (data) {
                if (data["status"]) {
                    $(hides).hide();
                    alert("删除成功");
                }
                else {
                    alert("请求失败");
                }
            });
        });
        $("#show_data").on("click", "#sell_makesure", function () {
            var postdata = {};
            postdata["method"] = "makesure"
            postdata["bookid"] = $(this).attr("bookid");
            var hides = this;
            $.post("/book/account_booksell/", postdata, function (data) {
                if (data["status"]) {
                    $(hides).hide();
                    $(hides).parent().children("#sell_refuse").hide();
                    alert("已确认交易");
                }
                else {
                    console.log("test");
                    alert("请求失败");
                }
            });
        });
    });
}

function Regist() {
    function CheckNull() {
        var num = 0;
        $("input").each(function (n) {
            if ($(this).val() == "") {
                num++;
            }
        });
        if (num > 0) {
            return true;
        }
        else {
            return false;
        }
    }
    $("document").ready(function () {
        $("form").submit(function (e) {
            if (CheckNull()) {
                e.preventDefault();
                $("#ErrorMessage").text("不能有空项！");
            }
        });
        $("input#login").click(function () {
            window.location.href = "/login/"
        });
        $("#check_code").click(function () {
            $(this).attr("src", "/check_code/?" + String(Math.random()));
            console.log("test");
        });
    });
}
/*
*
*  通用函数
*
*/

$("img").on("error", function (){
    $(this).attr("src", "/static/img/normal.jpg");
});

