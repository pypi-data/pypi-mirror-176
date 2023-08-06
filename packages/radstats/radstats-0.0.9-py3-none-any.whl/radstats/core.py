### Stephen Lawrence 2022

"""radiation effects system modeling tool

"""

__version__ = "0.0.9"

from lxml import etree
import schemdraw
from schemdraw import flow,logic,segments
from PIL import Image
import pickle
import numpy as np
import pandas as pd
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d
from scipy.special import erf
import sys
import itertools

# import ctypes
# os.system('cc -fPIC -shared -o bayes.o bayes.c')
# bayes = ctypes.CDLL('bayes.o')
from . import bayes

#####################################################################################################

class Box:
    """System element representing a logical combination of immediate subelements (a.k.a. children).

    Args:

        name (str): Unique identifier string for this :obj:`Box`.
        children (list): List of radstats.Effect or other radstats.Box objects that serve as inputs to this :obj:`Box`.
        gate (str): Logic gate descibing how the :obj:`Box` propagates values from its children.

    Returns:

        radstats.Box: Object representing the system element.

    """
    def __init__(self,name:str,children:list=[],gate:str='OR',**kwargs):
        ### initialize attributes
        self.name = name
        self.children = children
        self.gate = gate
        ### update attributes from kwargs
        self.__dict__.update(kwargs)


    def __str__(self):
        string = f"{repr(self)}\n{etree.tostring(self.XML(),encoding='unicode',pretty_print=True)}"
        for series in string.split('="[')[1:]:
            series = series.split(']"')[0]
            string = string.replace(series,f'{series.split()[0]} ... {series.split()[-1]}')
        return string


    def __repr__(self): return object.__repr__(self).replace(' at',f' "{self.name}" at')


    def __getitem__(self,name): return self.find(name)


    def XML(self):
        """Convert the :obj:`Box` to XML format.

        Returns:

            lxml.etree.Element: XML element representing the :obj:`Box` and its descendants.

        """
        xml = etree.Element('box',{'name':self.name,'gate':self.gate})
        for child in self.children: xml.append(child.XML())
        return xml


    def to_xml(self,file:str):
        """Export the :obj:`Box` to an XML file.

        Args:

            file (str): Path to save location.

        """
        open(file,'w').write(etree.tostring(self.XML(),encoding='unicode',pretty_print=True))


    def FT(self,file:str='ft.png',style=None,scale:int=3,shape:tuple=(3.5,1),spacing:tuple=(4,4),fontsize:int=36):
        """Generate a fault tree diagram of the :obj:`Box` and its descendants.

        Returns:

            :obj:`PIL.Image`: PIL-style Image object of the fault tree diagram.

        """
        system = self.XML()
        ### get element positions
        effects = system.xpath('.//*[local-name()="effect" or local-name()="ref"]')
        pos = {}
        for i,effect in enumerate(effects):
            pos[effect] = (i * spacing[0],-spacing[1] * len(effect.xpath('ancestor::box')))
        boxes = system.xpath('..//box')
        while len(boxes) > 0:
            for box in boxes:
                inputs = [i for i in box.xpath('*')]
                if all([i in pos.keys() for i in inputs]):
                    boxes.remove(box)
                    x = sum([pos[i][0] for i in inputs]) / len(inputs)
                    y = max([pos[i][1] for i in inputs]) + spacing[1]
                    pos[box] = (x,y)
        boxes = system.xpath('..//box')
        ### draw diagram
        schemdraw.config(inches_per_unit=scale,fontsize=fontsize*scale,lw=1.5*scale,font='Times New Roman') # monospace?
        with schemdraw.Drawing(file=file,show=False) as d:
            for effect in effects:
                [x,y] = shape
                label = effect.get('name')
                if len(label)/4 > x: x = len(label)/4
                if effect.tag == 'effect':
                    d += flow.Terminal(w=x,h=y).anchor('N').at(pos[effect]).label(label)
                if effect.tag == 'ref':
                    new = flow.Box(w=x,h=y).anchor('N').at(pos[effect]).label('\n'+label); d += new
                    new.segments.pop(0)
                    new.segments.append(segments.Segment([(0,-y/2),(x,-y/2)]))
                    new.segments.append(segments.Segment([(0,-y/2),(x/2,y/2)]))
                    new.segments.append(segments.Segment([(x/2,y/2),(x,-y/2)]))
            for box in boxes:
                [x,y] = shape
                label = box.get('name')
                if len(label)/4 > x: x = len(label)/4
                if box.get('name') in [n.get('name') for n in system.xpath('.//ref')]:
                    new = flow.Box(w=x,h=y).anchor('N').at(pos[box]).label('\n'+label); d += new
                    new.segments.pop(0)
                    new.segments.append(segments.Segment([(0,-y/2),(x,-y/2)]))
                    new.segments.append(segments.Segment([(0,-y/2),(x/2,y/2)]))
                    new.segments.append(segments.Segment([(x/2,y/2),(x,-y/2)]))
                else:
                    new = flow.Box(w=x,h=y).anchor('N').at(pos[box]).label(label); d += new
                if box.get('gate') == 'OR': new = logic.Or(inputs=1).at(new.S).down().reverse(); d += new
                if box.get('gate') == 'AND': new = logic.And(inputs=1).at(new.S).down().reverse(); d += new
                for sub in box.xpath('*'): d += flow.Wire('-|').at(new.in1).to(pos[sub])
        ### post process image
        image = Image.open(file)
        image.crop(image.getbbox())
        image.save(file)
        return image


    def find(self,name:str):
        """Find the first subelement of the :obj:`Box` matching a given :obj:`name`.

        Args:

            name (str): Unique name of desired element.

        Returns:

            radstats.Box or radstats.Effect: Subelement matching the given :obj:`name`.

        """
        for child in self.children:
            if child.name == name: return child
            elif type(child) == Effect: continue
            else:
                found = child.find(name)
                if found is not None: return found
        return None
    

    def find_all(self):
        """Find all subelements of the :obj:`Box`.

        Returns:

            list: List of radstats.Box and/or radstats.Effect representing all subelements.

        """
        children = []
        for child in self.children:
            if type(child) == Box: children.append(child.find_all())
            children.append([child])
        return list(itertools.chain.from_iterable(children))


    def import_rates(self,file):
        """Import Poisson event or dose accumulation rates from a CSV.

        Note: Element :obj:`rates` are overwritten with the CSV column where the header matches the :obj:`name` of the :obj:`Effect`.
        
        For example, if :obj:`rates.csv` looks like ::

            Effect1,Effect2,Effect3
            1,4,7
            2,5,8
            3,6,9

        The resulting rates for each effect will be ::

            Effect1.rates = [1,2,3]
            Effect2.rates = [4,5,6]
            Effect3.rates = [7,8,9]

        Args:

            file (str): path to properly formatted CSV file.

        Returns:

            radstats.Box: The object that called the function, after the rates have been updated (in place).

        """
        df = pd.read_csv(file)
        for name in df.columns:
            child = self.find(name)
            if child is not None: child.rate = df[name].to_numpy()
        return self


    def Q(self,time:list,subset:list=None,force:dict={}):
        """Compute the unavailability of the :obj:`Box` and its descendants given a time index.

        Unavailability :math:`Q(t)` is the probability that an element is in a non-functional state at a certain time.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            subset (list): List of system elements for limiting the analysis, defaults to :obj:`self.find_all()`.
            force (dict): Force a certain unavailability on specific elements, formatted as :obj:`{name:forced_Q}`.

        Returns:

            radstats.PFrame: Probabilistic DataFrame containing the analysis results along with the time index. See radstats.PFrame documentation for further analysis options.

        """
        q = PFrame({'Time':time},owner=self).set_index('Time')
        if subset is None: subset = self.find_all()
        if self.name in force.keys(): q[self.name] = force[self.name]
        else:
            for child in self.children:
                if child in subset: q = q.join(child.Q(time,subset,force))
            fx = getattr(sys.modules['radstats.bayes'],self.gate)
            q[self.name] = [fx([q[child.name][t] for child in self.children if child in subset]) for t in time]
        # if children_only: q = q[[child.name for child in inputs] + [self.name]]
        return q


    def _recoverable(self): return False


    def F(self,time:list,subset:list=None):
        """Compute the unreliability of the :obj:`Box` and its descendants given a time index.

        Unreliability :math:`F(t)` is the probability that an element has permanently failed by a certain time.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            subset (list): List of system elements for limiting the analysis, defaults to :obj:`self.find_all()`.

        Returns:

            radstats.PFrame: Probabilistic DataFrame containing the analysis results along with the time index. See radstats.PFrame documentation for further analysis options.

        """
        if subset is None: subset = self.find_all()
        subset = [sub for sub in subset if sub._recoverable() == False]
        return self.Q(time,subset)


    def sim(self,time:list,N:int):
        """Perform a Monte Carlo simulation of the system with N runs over the given time index

        The results of this method are accessed from the returned dict via keys.

            - Key :obj:`Q`: simulated unavailability :math:`Q_{sim}(t)` with time as the index.
            - Key :obj:`F`: simulated unreliability :math:`F_{sim}(t)` with time as the index.
            - Key :obj:`T`: failure times :math:`T_{fail}(n)` for each element, with the run number as the index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            N (int): Number of runs to simulate. More runs results in greater accuracy but takes longer.

        Returns:

            dict: Dictionary of pandas.DataFrame objects with result accessible via keys :obj:`{Q,F,T}`.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        f = pd.DataFrame({'Time':time}).set_index('Time')
        t = pd.DataFrame({'Run':range(N)}).set_index('Run')
        for child in self.children:
            sub_sim = child.sim(time,N)
            q = q.join(sub_sim['Q'])
            f = f.join(sub_sim['F'])
            t = t.join(sub_sim['T'])
        fx = getattr(sys.modules['radstats.bayes'],self.gate)
        q[self.name] = [fx([q[child.name][t] for child in self.children]) for t in time]
        subset = [sub for sub in self.find_all() if sub._recoverable() == False]
        f[self.name] = [fx([f[child.name][t] for child in self.children if child in subset]) for t in time]
        return {'Q':q,'F':f,'T':t}

#####################################################################################################

class Effect:
    """System element representing a radiation-induced failure mode.

    Args:

        name (str): Unique identifier string for this Effect.
        type (str): Type of effect (:obj:`SEE`, :obj:`TID`, or :obj:`DDD`). If :obj:`None`, the effect type will be deduced based on the :obj:`name`.
        rate (float or iterable): Poisson event rate :math:`\lambda(t)` or dose accumulation rate :math:`\dot{D}(t)` (per second).

    Returns:

        radstats.Effect: Object representing the system element.

    Keyword Args:

        mttr (float): Mean Time To Repair :math:`1/\mu_r` (in seconds), if any -- only relevant for SEE.
        mean (float): Lognormal mean :math:`\mu_{\ln}` of failure doses -- only relevant for TDE.
        sd (float): Lognormal standard deviation :math:`\sigma_{\ln}` of failure doses -- only relevant for TDE.

    """
    def __init__(self,name:str,type:str=None,rate:float=0,**kwargs):
        ### initialize attributes
        self.name = name
        self.type = type
        self.rate = rate
        if type is None:
            if 'SEL' in self.name: self.type = 'SEE'
            elif 'SEFI' in self.name: self.type = 'SEE'
            elif 'DSEE' in self.name: self.type = 'SEE'
            elif 'TID' in self.name: self.type = 'TID'
            elif 'DDD' in self.name: self.type = 'DDD'
        ### update attributes from kwargs
        self.__dict__.update(kwargs)
        

    def __str__(self):
        string = f"{repr(self)}\n{etree.tostring(self.XML(),encoding='unicode',pretty_print=True)}"
        for series in string.split('="[')[1:]:
            series = series.split(']"')[0]
            string = string.replace(series,f'{series.split()[0]} ... {series.split()[-1]}')
        return string


    def __repr__(self): return object.__repr__(self).replace(' at',f' "{self.name}" at')
    

    def XML(self):
        """Convert :obj:`Effect` to an XML format.

        Returns:

            lxml.etree.Element: XML element object representing the :obj:`Effect`.

        """
        return etree.Element('effect',{k:str(v) for k,v in self.__dict__.items()})
    

    def to_xml(self,file:str):
        """Export the :obj:`Effect` to an XML file.

        Args:
            file (str): Path to save location.

        """
        open(file,'w').write(etree.tostring(self.XML(),encoding='unicode',pretty_print=True))


    def import_rates(self,file:str):
        """Import Poisson event or dose accumulation rates from a CSV.

        Note: Element rates are overwritten with the CSV column where the header matches the :obj:`name` of the :obj:`Effect`.
        
        For example, if :obj:`rates.csv` looks like ::

            Effect1,Effect2,Effect3
            1,4,7
            2,5,8
            3,6,9

        The resulting rates for each effect will be ::

            Effect1.rate = [1,2,3]
            Effect2.rate = [4,5,6]
            Effect3.rate = [7,8,9]

        Args:

            file (str): path to properly formatted CSV file.

        """
        df = pd.read_csv(file)
        if self.name in df.columns: self.rate = df[self.name].to_numpy()


    def _recoverable(self):
        if hasattr(self,'mttr'):
            if self.mttr not in [None,np.nan,np.inf]: return True
        return False


    def Q(self,time:list,subset:list=None,force={}):
        """Compute the unavailability :math:`Q(t)` of the :obj:`Effect` given a time index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            force (dict): Force a certain unavailability on specific elements, formatted as :obj:`{name:forcedQ}`.

        Returns:

            radstats.PFrame: Probabilistic DataFrame containing the analysis results along with the time index. See radstats.PFrame documentation for further analysis options.

        """
        q = PFrame({'Time':time}).set_index('Time')
        if self.name in force.keys(): q[self.name] = force[self.name]
        else:
            if self.type == 'SEE':
                rate = _rescale(np.array(self.rate),time)
                if self._recoverable(): q[self.name] = rate/(rate+_rescale(1/float(self.mttr),time))
                else: q[self.name] = 1 - np.exp(-cumtrapz(rate,time,initial=0))
            elif self.type == 'TID':
                rate = _rescale(np.array(self.rate),time)
                dose = cumtrapz(rate,time,initial=1e-15)
                q[self.name] = (1/2)*(1+erf((np.log(dose)-float(self.mean))/(float(self.sd)*np.sqrt(2))))
        return q


    def F(self,time:list,subset:list=None):
        """Compute the unreliability of the :obj:`Effect` given a time index.

        Unreliability :math:`F(t)` is the probability that an element has permanently failed by a certain time.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            subset (list): List of system elements for limiting the analysis, defaults to :obj:`self.find_all()`.

        Returns:

            radstats.PFrame: Probabilistic DataFrame containing the analysis results along with the time index. See radstats.PFrame documentation for further analysis options.

        """
        return self.Q(time) if self._recoverable() == False else self.Q(time,force={self.name:0})


    def sim(self,time,N):
        """Perform a Monte Carlo simulation of the system with N runs over the given time index

        The results of this method are accessed from the returned dict via keys.

            - Key :obj:`Q`: simulated unavailability :math:`Q_{sim}(t)` with time as the index.
            - Key :obj:`F`: simulated unreliability :math:`F_{sim}(t)` with time as the index.
            - Key :obj:`T`: failure times :math:`T_{fail}(n)` for each element, with the run number as the index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            N (int): Number of runs to simulate. More runs results in greater accuracy but takes longer.

        Returns:

            dict: Dictionary of pandas.DataFrame objects with result accessible via keys :obj:`{Q,F,T}`.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        f = pd.DataFrame({'Time':time}).set_index('Time')
        t = pd.DataFrame({'Run':range(N)}).set_index('Run')
        q[self.name] = np.nan
        if self.type == 'SEE':
            rate = _rescale(np.array(self.rate),time)
            if self._recoverable():
                x = cumtrapz(rate,time,initial=0)
                nfail = np.random.poisson(x[-1],N) # number of events
                curve = interp1d(x,time,fill_value='extrapolate')
                tfail = curve(np.random.uniform(min(x),max(x),(N,max(nfail))))
                for n in range(N): 
                    tfail[n][nfail[n]:] = np.nan
                    for m in tfail[n]: # remove overlapping events
                        tfail[n][np.logical_and(tfail[n] > m,tfail[n] < m + float(self.mttr))] = np.nan
                    tfail[n].sort()
                t[self.name] = [' '.join(np.around(i[~np.isnan(i)],3).astype(str)) for i in tfail]
                trepair = tfail + float(self.mttr)
                for i in q.index: q[self.name][i] = (sum(sum(tfail <= i)) - sum(sum(trepair <= i)))
            else: 
                x = cumtrapz(rate,time,initial=0)
                curve = interp1d(x,time,fill_value='extrapolate')
                tfail = curve(np.random.exponential(1,N))
                t[self.name] = tfail
                for i in q.index: q[self.name][i] = sum(tfail < i)
        elif self.type == 'TID':
            rate = _rescale(np.array(self.rate),time)
            dose = cumtrapz(rate,time,initial=1e-15)
            curve = interp1d(dose,time,fill_value='extrapolate')
            dfail = np.random.lognormal(float(self.mean),float(self.sd),N)
            tfail = curve(dfail)
            t[self.name] = tfail
            for i in q.index: q[self.name][i] = sum(tfail < i)
        q[self.name] = q[self.name] / N
        if self._recoverable() == False: f[self.name] = q[self.name]
        return {'Q':q,'F':f,'T':t}

#####################################################################################################

class PFrame(pd.DataFrame):
    """Custom subclass of pandas.DataFrame allowing further analysis of results.

    """
    def __init__(self,*args,**kwargs):
        self.owner = kwargs.pop('owner',None)
        super().__init__(*args,**kwargs)

    _metadata = ['owner']
    @property
    def _constructor(self):
        def _c(*args, **kwargs):
            return PFrame(*args, **kwargs).__finalize__(self)
        return _c
    
    def I(self):
        """Compute importance and worth metrics of the :obj:`Box` and its descendants given a time index.

        The results of this method are accessed from the returned dict via keys.

            - Item :obj:`[0]` is marginal importance :math:`I_M(t)=P_t(Z|A)-P_t(Z|A')`
            - Item :obj:`[1]` is critical importance :math:`I_C(t)=I_M(t) P_t(A)/P_t(Z)`
            - Item :obj:`[2]` is risk achievement worth :math:`\mathcal{A}(t)=P_t(Z|A)-P_t(Z)`
            - Item :obj:`[3]` is risk reduction worth :math:`\mathcal{D}(t)=P_t(Z|A')-P_t(Z)`

        Where :math:`Z` is the :obj:`Box` calling the function and and :math:`A` is a descendant.

        """
        raw = pd.DataFrame(index=self.index)
        rrw = pd.DataFrame(index=self.index)
        im = pd.DataFrame(index=self.index)
        ic = pd.DataFrame(index=self.index)
        subset = [sub for sub in self.owner.find_all() if sub.name in self.columns]
        for col in self.columns:
            Qoff = self.owner.Q(self.index,subset,{col:1})[self.owner.name]
            Qon = self.owner.Q(self.index,subset,{col:0})[self.owner.name]
            raw[col] = np.subtract(Qoff,self[self.owner.name])
            rrw[col] = np.subtract(Qon,self[self.owner.name])
            im[col] = np.subtract(Qoff,Qon)
            ic[col] = im[col] * np.divide(self[col],self[self.owner.name]+1e-15)
        return im,ic,raw,rrw
    
    def IM(self): 
        """Marginal importance (alias for I()[0])
        
        """
        return self.I()[0]

    def IC(self):
        """Critical importance (alias for I()[1])
        
        """
        return self.I()[1]

    def RAW(self):
        """Risk achievement worth (alias for I()[2])
        
        """
        return self.I()[2]

    def RRW(self):
        """Risk reduction worth (alias for I()[3])

        """
        return self.I()[3]

#####################################################################################################

def _rescale(y:list,x:list):
    """Rescales vector :obj:`y` over horizontal axis :obj:`x`.

    Note: Assumes both vectors are linear. Also accepts float or int for :obj:`y`.

    Args:

        y (iterable, float, or int): Arbitrary value or list of values.
        x (iterable): New horizontal axis over which to interpolate :obj:`y`.

    Returns:
    
        iterable: Vector aligned with :obj:`y`, but with the same length as :obj:`x`.

    """
    try: n = len(y)
    except TypeError: y = [y,y]; n = len(y)
    interp = interp1d(np.linspace(0,1,n),y)
    return interp(x / max(x))


def _parse_xml(element:etree.Element):
    """Converts an radstats-formatted XML element into a radstats.Box or radstats.Effect object.

    Args:

        element (lxml.etree.Element): Properly formatted XML element.

    Returns:
    
        radstats.Box or radstats.Effect: radstats system element parsed from the XML element.

    """
    if element.tag == 'effect': return Effect(**element.attrib)
    elif element.tag == 'box':
        box = Box(**element.attrib)
        box.children = [_parse_xml(child) for child in element]
        return box


def from_xml(file:str):
    """Converts a radstats-formatted XML file into a radstats.Box representing the system model.

    Args:

        file (str): Path to properly formatted XML file.

    Returns:
    
        radstats.Box: Top-level element for the system model.

    """
    tree = etree.parse(file)
    root = tree.getroot()
    return _parse_xml(root)