### Stephen Lawrence 2022

"""Radiation effects system modeling tool

"""

__version__ = "0.0.8"

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


    def FT(self,file:str='ft.png',scale:int=3,shape:tuple=(3.5,1),spacing:tuple=(4,4),fontsize:int=36):
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


    def Q(self,time:list,file:str=None,children_only=False,force={}):
        """Compute the unavailability :math:`Q(t)` of the :obj:`Box` and its descendants given a time index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            file (str): File to optionally save the results in CSV format.
            children_only (bool): Limit the analysis to only immediate subelements.
            force (dict): Force a certain unavailability on specific elements, formatted as :obj:`{name:forced_Q}`.

        Returns:

            pd.DataFrame: Dictionary of lists containing the analysis results along with the time index.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        if self.name in force.keys(): q[self.name] = force[self.name]
        else:
            for child in self.children: q = q.join(child.Q(time,force=force))
            f = getattr(sys.modules['radstats.bayes'],self.gate)
            q[self.name] = [f([q[child.name][t] for child in self.children]) for t in time]
        if children_only: q = q[[child.name for child in self.children]]
        if file is not None: q.to_csv(file)
        return q


    def I(self,time:list,file:str=None,children_only=False):
        """Compute importance and worth metrics of the :obj:`Box` and its descendants given a time index.

        The results of this method are accessed from the returned dict via keys.

            - :obj:`M`: Marginal importance :math:`I_M(t)=P_t(Z|A)-P_t(Z|A')`
            - :obj:`C`: Critical importance :math:`I_C(t)=I_M(t) P_t(A)/P_t(Z)`
            - :obj:`RAW`: Risk achievement worth :math:`\mathcal{A}(t)=P_t(Z|A)-P_t(Z)`
            - :obj:`RRW`: Risk reduction worth :math:`\mathcal{D}(t)=P_t(Z|A')-P_t(Z)`

        Where :math:`Z` is the :obj:`Box` calling the function and and :math:`A` is a descendant.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            file (str): File to optionally save the results in CSV format.
            children_only (bool): Limit the analysis to only immediate subelements.

        Returns: 

            dict: Dictionary of pandas.DataFrame objects with each importance metric accessible by a key :obj:`{M,C,RAW,RRW}`.
    
        """
        Q = self.Q(time)
        raw = pd.DataFrame(index=Q.index)
        rrw = pd.DataFrame(index=Q.index)
        im = pd.DataFrame(index=Q.index)
        ic = pd.DataFrame(index=Q.index)
        if children_only: subelements = self.children + [self]
        else: subelements = self.find_all() + [self]
        for sub in subelements:
            yesQ = self.Q(time,force={sub.name:1})[self.name]
            notQ = self.Q(time,force={sub.name:0})[self.name]
            raw[sub.name] = np.subtract(yesQ,Q[self.name])
            rrw[sub.name] = np.subtract(notQ,Q[self.name])
            im[sub.name] = np.subtract(yesQ,notQ)
            ic[sub.name] = im[sub.name] * np.divide(Q[sub.name],Q[self.name]+1e-15)
        return {'M':im,'C':ic,'RAW':raw,'RRW':rrw}

    def sim(self,time:list,N:int):
        """Perform a Monte Carlo simulation of the system with N runs over the given time index

        The results of this method are accessed from the returned dict via keys.

            - Key :obj:`Q`: simulated unavailability :math:`Q_{\text{sim}}(t)` with time as the index.
            - Key :obj:`T`: failure times :math:`T_{\text{fail}}(n)` for each element, with the run number as the index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            N (int): Number of runs to simulate. More runs results in greater accuracy but takes longer.

        Returns:

            dict: Dictionary of pandas.DataFrame objects with result accessible via keys :obj:`{Q,T}`.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        t = pd.DataFrame({'Run':range(N)}).set_index('Run')
        for child in self.children:
            sub_sim = child.sim(time,N)
            q = q.join(sub_sim['Q'])
            t = t.join(sub_sim['T'])
        f = getattr(sys.modules['radstats.bayes'],self.gate)
        q[self.name] = [f([q[child.name][t] for child in self.children]) for t in time]
        return {'Q':q,'T':t}

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
    

    def Q(self,time:list,file:str=None,force={}):
        """Compute the unavailability :math:`Q(t)` of the :obj:`Effect` given a time index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            file (str): File to optionally save the results in CSV format.
            force (dict): Force a certain unavailability on specific elements, formatted as :obj:`{name:forcedQ}`.

        Returns:

            dict: Dictionary of lists containing the analysis results along with the time index.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        if self.name in force.keys(): q[self.name] = force[self.name]
        else:
            if self.type == 'SEE':
                rate = rescale(np.array(self.rate),time)
                if hasattr(self,'mttr'): q[self.name] = rate/(rate+rescale(1/float(self.mttr),time))
                else: q[self.name] = 1 - np.exp(-cumtrapz(rate,time,initial=0))
            elif self.type == 'TID':
                rate = rescale(np.array(self.rate),time)
                dose = cumtrapz(rate,time,initial=1e-15)
                q[self.name] = (1/2)*(1+erf((np.log(dose)-float(self.mean))/(float(self.sd)*np.sqrt(2))))
        if file is not None: q.to_csv(file)
        return q

    def sim(self,time,N):
        """Perform a Monte Carlo simulation of the system with N runs over the given time index

        The results of this method are accessed from the returned dict via keys.

            - Key :obj:`Q`: simulated unavailability :math:`Q_{\text{sim}}(t)` with time as the index.
            - Key :obj:`T`: failure times :math:`T_{\text{fail}}(n)` for each element, with the run number as the index.

        Args:

            time (iterable): Numerical time index for the analysis (in seconds).
            N (int): Number of runs to simulate. More runs results in greater accuracy but takes longer.

        Returns:

            dict: Dictionary of pandas.DataFrame objects with result accessible via keys :obj:`{Q,T}`.

        """
        q = pd.DataFrame({'Time':time}).set_index('Time')
        t = pd.DataFrame({'Run':range(N)}).set_index('Run')
        q[self.name] = np.nan
        if self.type == 'SEE':
            rate = rescale(np.array(self.rate),time)
            if hasattr(self,'mttr'):
                x = cumtrapz(rate,time,initial=0)
                nfail = np.random.poisson(x[-1],N) # number of events
                curve = interp1d(x,time,fill_value='extrapolate')
                tfail = curve(np.random.uniform(min(x),max(x),(N,max(nfail))))
                for n in range(N): 
                    tfail[n][nfail[n]:] = np.nan
                    tfail[n].sort()
                    for m in tfail[n]: # remove overlapping events
                        tfail[n][np.logical_and(tfail[n] > m,tfail[n] < m + float(self.mttr))] = np.nan
                    tfail[n].sort()
                t[self.name] = list(tfail)
                trepair = tfail + float(self.mttr)
                for i in q.index: q[self.name][i] = (sum(sum(tfail <= i)) - sum(sum(trepair <= i)))
            else: 
                x = cumtrapz(rate,time,initial=0)
                curve = interp1d(x,time,fill_value='extrapolate')
                tfail = curve(np.random.exponential(1,N))
                t[self.name] = tfail
                for i in q.index: q[self.name][i] = sum(tfail < i)
        elif self.type == 'TID':
            rate = rescale(np.array(self.rate),time)
            dose = cumtrapz(rate,time,initial=1e-15)
            curve = interp1d(dose,time,fill_value='extrapolate')
            dfail = np.random.lognormal(float(self.mean),float(self.sd),N)
            tfail = curve(dfail)
            t[self.name] = tfail
            for i in q.index: q[self.name][i] = sum(tfail < i)
        q[self.name] = q[self.name] / N
        return {'Q':q,'T':t}

#####################################################################################################

def rescale(y:list,x:list):
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


def parse_xml(element:etree.Element):
    """Converts an radstats-formatted XML element into a radstats.Box or radstats.Effect object.

    Args:

        element (lxml.etree.Element): Properly formatted XML element.

    Returns:
    
        radstats.Box or radstats.Effect: radstats system element parsed from the XML element.

    """
    if element.tag == 'effect': return Effect(**element.attrib)
    elif element.tag == 'box':
        box = Box(**element.attrib)
        box.children = [parse_xml(child) for child in element]
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
    return parse_xml(root)