$.ajax({
    type: type,
    url: url,
    data: data,
    dataType: 'json',
    success: function (result) {

    },
    error: function () {

    },
})

name = $(this).parents('tr').children('td').eq(0).text() //获取页面元素,按钮的父元素tr的子元素td的第0个元素的文本

$('#selectbooks input[type="checkbox"]').each(function(){  //取出所有input checkbox类型的元素
            if (this.checked == true) {  #判断是否选中
                bookids.push($(this).attr('bookid'))  #选中则加入bookids数组
            }

        })


#以下代码修改于源码list.py，用于删除最后一面所有数据后，自动跳转到前一页，而不是返回404

def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
        except InvalidPage as e:
            page = paginator.page(paginator.num_pages)
        return (paginator, page, page.object_list, page.has_other_pages())


#radio单选按钮change事件