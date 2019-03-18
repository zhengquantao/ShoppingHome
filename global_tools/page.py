class Page():
    def __init__(self, page_num, total_count, url_prefix, per_page=10, max_page=8):
        self.url_prefix = url_prefix
        # 每一页显示多少条数据
        # 每一页数据数
        self.per_page = per_page
        # 总页码展示数
        total_page, m = divmod(total_count, self.per_page)
        if m:
            total_page += 1
            self.total_page = total_page
        # 从url中取参数
        try:
            self.page_num = int(page_num)
            # 当输入页数大于最后一页 默认返回最后一页
            if self.page_num > total_page:
                self.page_num = total_page
        except Exception as e:
            # 当输入不正经数字 默认返回第一页
            page_num = 1
            self.page_num = page_num
        # 定义两个变量保存数据从哪到哪
        self.data_start = (self.page_num - 1) * per_page  # 没有传就用默认的展示10个
        self.data_end = self.page_num * per_page  # 没有传就用默认的展示10个
        # 页面上共展示多少页码
        self.max_page = max_page
        if total_page < max_page:
            max_page = total_page
        half_max_page = max_page // 2
        # 页面上展示的页码从哪里开始
        page_start = self.page_num - half_max_page
        # 页面展示的页码到哪里结束
        page_end = self.page_num + half_max_page
        if page_start <= 1:
            page_start = 1
            page_end = max_page
        if page_end >= total_page:
            page_end = total_page
            page_start = total_page - max_page + 1
        self.page_start = page_start
        self.page_end = page_end

    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end

    def page_html(self):
        # 自己并接分业务的HTML代码
        html_list = []
        # 加上首页
        html_list.append('<li><a href="{}&page=1">首页</a></li>'.format(self.url_prefix))
        # 加上上一页
        if self.page_num <= 1:
            html_list.append('<li class="disabled><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_list.append('<li><a href="{}&page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                self.url_prefix, self.page_num - 1))
        for i in range(self.page_start, self.page_end+1):
            # 如果是当前页就加一个active样式类
            if i == self.page_num:
                tmp = '<li class="active"><a href="{0}&page={1}">{1}</a></li>'.format(self.url_prefix, i)
            else:
                tmp = '<li><a href="{0}&page={1}">{1}</a></li>'.format(self.url_prefix, i)
            html_list.append(tmp)
        # 加上下一页
        if self.page_num >= self.total_page:
            html_list.append('<li class="disabled><a href="#"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_list.append(
                '<li><a href="{}&page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix,
                                                                                                   self.page_num + 1))
        # 加最尾页
        html_list.append('<li><a href="{}&page={}">尾页</a></li>'.format(self.url_prefix, self.total_page))
        page_html = ''.join(html_list)
        return page_html