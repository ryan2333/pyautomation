#ajax请求示例
$.ajax({
    type: type,  #请求类型，post,put,delete,get等
    url: url,   #请求发到后端的url，即后端接收请求的url
    data: data,  #发送的数据
    dataType: json, #发送数据类型，一般使用json
    async: false,  //是否同步，同步为false，异步为true,默认为异步
    success: function(data){
        console.log(data)
    },
    error: function(data){
        console.log(err)
    },

})


#使用同步ajax场景：当后续代码依赖上一步的结果，就需要阻塞即同步方式
    1。 点击按钮，从后端获取权限数据
    2。 通过则ajax发送页面数据到后端，不通过则提示无权限