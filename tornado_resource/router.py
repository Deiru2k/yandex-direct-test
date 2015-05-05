from collections import OrderedDict


class Router:
    
    resources = OrderedDict()
    
    def __init__(self, version):
        self.version = version
    
    def add_resource(self, resource):
        name = ".".join(construct_name(resource))
        resource = {
            "object": resource,
            "url": resource.url
        }
        self.resources[name] = resource
    
    def get_url(self, name):
        resource = self.resources.get(name, None)
        if not resource: return resource
        return "/%s%s" % (self.version, "".join(construct_url(resource['object'])))
        
        
    @property
    def routes(self):
        return [ 
            ("/%s%s" % (self.version, ''.join(construct_url(self.resources[key]['object']))), self.resources[key]['object']) for key in self.resources
        ]
            

def construct_url(resource):
    path = list()
    path.append(resource.url)
    if hasattr(resource, "parent"): path += construct_url(resource.parent)
    path.reverse()
    return path
    

def construct_name(resource, root=True):
    path = list()
    name = resource.name
    if not name: name = resource.__name__
    else: root = False
    path.append(name)
    if hasattr(resource, 'parent'):
        path += construct_name(resource.parent, root=False)
    path.reverse()
    if root: path.insert(0, resource.__module__.split(".")[-1])
    return path
