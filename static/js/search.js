window.onload = function () {

            function showmore(contentid) {
                var len = 130;      //默认显示字数
                var ctn = document.getElementsByClassName(contentid);  //获取div对象
                for (let i = 0; i < ctn.length; i++) {
                    let content = ctn[i].innerHTML;                   //获取div里的内容

                    let span = document.createElement("span");     //创建<span>元素
                    let a = document.createElement("a");           //创建<a>元素
                    span.innerHTML = content.substring(0, len);     //span里的内容为content的前len个字符

                    a.innerHTML = content.length > len ? "... 展开" : "";  ////判断显示的字数是否大于默认显示的字数    来设置a的显示
                    a.href = "javascript:void(0)";//让a链接点击不跳转

                    a.onclick = function () {
                        if (a.innerHTML.indexOf("展开") > 0) {      //如果a中含有"展开"则显示"收起"
                            a.innerHTML = "<<&nbsp;收起";
                            span.innerHTML = content;
                        } else {
                            a.innerHTML = "... 展开";
                            span.innerHTML = content.substring(0, len);
                        }
                    }
                    // 设置div内容为空，span元素 a元素加入到div中
                    ctn[i].innerHTML = "";
                    ctn[i].appendChild(span);
                    ctn[i].appendChild(a);
                }

            }

            document.getElementById("findButton").onclick = function () {
                //防在send()这个函数小括号里的数据，会自动在请求体中提交
                let text = document.getElementById("textId").value;
                if (!text) {
                    alert("请输入要查找的内容");
                    document.getElementById("div_box").innerHTML = null
                    return
                }
                //1、创建Ajax核心对象
                let xhr = new XMLHttpRequest();
                //    2、注册回调函数
                xhr.onreadystatechange = function () {
                    if (this.readyState === 4) {
                        if (this.status !== 200) {
                            alert(this.status);
                        } else {
                            //通过XMLHttpRequest函数的responseText属性可以获取服务器响应来的数据
                            let datas = JSON.parse(this.responseText);
                            let searchDatas = datas.data
                            let html = "";
                            for (let i = 0; i < searchDatas.length; i++) {
                                html += "<hr>"
                                html += "<div class='data'>"
                                html += "id: " + searchDatas[i].id + ", fullText: " + searchDatas[i].fullText + ", accusation: " + searchDatas[i].accusation
                                html += "</div>"
                            }
                            console.log(html)
                            document.getElementById("div_box").innerHTML = html
                            showmore('data')
                        }
                    }
                }

                //3、开启通道
                xhr.open("POST", "/search", true)

                //4、发送请求
                //怎么模拟ajax提交form表单呢 ? 设置请求头的类型（这行代码非常关键，是模拟提交form表单的关键代码）
                //设置请求头的内容类型时必须在open的后面
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")

                //send("注意格式：放在这里的数据就是在请求体中提交的，格式不能乱来，要遵从Http协议来写")
                xhr.send("search=" + text);
            }
        }