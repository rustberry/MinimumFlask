import json

from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    """
    The big ORM
    """
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了
        if index == -1:
            pass
        else:
            models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        # log('debug save')
        models = self.all()
        # log('models', models)
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                # log('m', m)
                self.id = m.id + 1
            models.append(self)
        else:
            # index = self.find(self.id)
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log('debug', index)
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


class Post(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')

    def comments(self):
        # return [c for c in Comment.all() if c.tweet_id == self.id]
        return Comment.find_all(post_id=self.id)

    @classmethod
    def new(cls, form):
        p = cls(form)
        p.save()
        return p


class Comment(Model):
    def __init__(self, form):
        self.id = form.get('id', -1)
        self.content = form.get('content', '')
        self.post_id = form.get('post_id', -1)

    @classmethod
    def new(cls, form):
        c = cls(form)
        c.save()
        return c


def test_tweet():
    form = {
        'content': 'hello tweet'
    }
    t = Tweet(form, 1)
    t.save()
    form = {
        'content': 'right yeah'
    }
    c = Comment(form, 2)
    c.tweet_id = 1
    c.save()
    t = Tweet.find(1)
    print('comments, ', t.comments())
    pass

def test_read():
    todos = Tweet.all()
    # log('test read', todos)
    t = Tweet.find(1)
    assert t is not None, 't is none'
    assert t.id == 1, 'id error'

def test():
    test_tweet()
    test_read()


if __name__ == '__main__':
    test()
