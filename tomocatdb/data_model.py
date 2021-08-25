from sqlalchemy import MetaData, Column, Date, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import declarative_base, validates, relationship
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB, json
from sqlalchemy.sql.sqltypes import Boolean

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })
Base = declarative_base(metadata=meta)

#### MATERIALS ####

# Zeolites
class Zeolites(Base):
    '''
    ORM class representing a table of zeolite materials. 
    -------------
    DESCRIPTION
    supplier_id : the label name given by the supplier
    supplier : the supplier name
    sar : Silicon/Aluminium - Ratio
    framework : the framework abbreviation type i.e. BEA.
    water_content : the weight pct of water
    --------------
    RELATIONSHIPS
    extrudates : one-to-many
    samples : one-to-many
    '''
    __tablename__ = 'zeolites'
    
    id = Column(Integer, primary_key=True)
    supplier_id = Column(String(30), nullable=False)
    internal_id = Column(String, unique=True, nullable=False)
    supplier = Column(String(30))
    sar = Column(Float(precision=2))
    framework = Column(String(30), nullable=False)

    # Child relationships one-to-many
    catalytic_tests = relationship("CatalyticTesting")

    gas_analysis = relationship("GasAdsorptionAnalysis")
    tg_analysis = relationship("tgAnalysis")
    xrdexsitu_analysis = relationship("xrdExSituAnalysis")
    
    def __repr__(self):
        return (f"Zeolite(id={self.id!r}, internal_id={self.internal_id!r}, supplier_id={self.supplier_id!r}, producer={self.supplier!r}"
                + f", sar={self.sar!r}, framework={self.framework!r})")
    
    @validates('supplier_id', 'framework')
    def convert_upper(self, key, value):
        return value.upper()

# Extrudates

class Extrudates(Base):
    '''
    ORM class representing a table of extrudate materials
    --------------
    DESCRIPTION
    zeolite_id : ForeignKey from Zeolites
    zeolite_framework : ForeignKey from Zeolites
    alumina_wpct : weight pct of alumina in extrudates
    dopant : dopant type in weight pct
    dopant_wpct : dopant weight pct in the extrudate
    --------------
    RELATIONSHIPS
    zeolites : many-to-one
    samples : many-to-one
    '''
    __tablename__ = 'extrudates'
    
    id = Column(Integer, primary_key=True)
    internal_id = Column(String, nullable=False, unique=True)
    zeolite_id = Column(String, ForeignKey('zeolites.internal_id'), nullable=False)
    zeolite_framework = Column(String, nullable=False)
    alumina_wpct = Column(Integer)
    dopant = Column(String)
    supplier = Column(String)
    manufacturing_method = Column(String)
    shape = Column(String)
        
    # Relationships one-to-many
    catalytic_tests = relationship("CatalyticTesting")

    gas_analysis = relationship("GasAdsorptionAnalysis")
    tg_analysis = relationship("tgAnalysis")
    xrdexsitu_analysis = relationship("xrdExSituAnalysis")
    
    def __repr__(self):
        return (f"Extrudates(id={self.id!r}, zeolite_id={self.zeolite_id!r}, zeolite_framework={self.zeolite_framework!r}" 
               + f", alumina_wpct={self.alumina_wpct!r}, dopant={self.dopant!r})")    

    
###### Catalytic Information ######

class ReactorSamples(Base):
    '''
    ORM class representing a table of Sample_Reactor_Layer
    --------------
    DESCRIPTION
    layer : layer type ('t', 'm', 'b')
    --------------
    RELATIONSHIPS
    samples : one-to-many
    '''
    
    __tablename__ = 'reactor_samples'
    
    id = Column(Integer, primary_key=True)
    testing_code = Column(String, ForeignKey('catalytic_testing.code'), nullable=False, unique=False)
    layer_code = Column(String, nullable=False, unique=True)
    reactor_layer = Column(String)
    identifier = Column(Integer)
    sample_mass = Column(Integer)
    
    #__tableargs__ = (ForeignKeyConstraint([testing_code], ['catalytic_testing.code']),)
    
    # MANY-TO-ONE relationships
    catalytic_test = relationship("CatalyticTesting", back_populates='reactor_samples')

    # ONE-TO-MANY relationships
    gas_analysis = relationship("GasAdsorptionAnalysis")
    tg_analysis = relationship("tgAnalysis")
    xrdexsitu_analysis = relationship("xrdExSituAnalysis")
    
    @validates('reactor_layer')
    def validate_reactor_layer(self, key, value):
        if value.lower() in ['top', 'middle', 'bottom']:
            return value.lower()
        else:
            raise AssertionError("Not a valid reactor layer, should be one of: 'top', 'middle', 'bottom'.")
    
    def __repr__(self):
        return f"Sample(id={self.id!r}, run_code={self.testing_code!r}, layer_code={self.reactor_layer!r} ,,reactor_layer={self.reactor_layer!r})"


class CatalyticTesting(Base):
    '''
    ORM class of catalytic testing table
    '''
    
    __tablename__ = 'catalytic_testing'
    
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    extrudate_id = Column(String, ForeignKey('extrudates.internal_id'))    
    zeolite_id = Column(String, ForeignKey('zeolites.internal_id'))    
    reaction_id = Column(String, ForeignKey('catalytic_reactions.reaction'))
    state_of_deactivation = Column(String)
    deactivation_degree = Column(Float)
    tos = Column(Float)
    whsv = Column(Float)
    catalyst_mass = Column(Float)
    bed_height = Column(Float)
    diluent_mass = Column(Float)
    creation_date = Column(Date, default=func.now())
    
    reactor_samples = relationship("ReactorSamples", back_populates='catalytic_test')  
    
    @validates('state_of_deactivation')
    def validate_state_of_deactivation(self, key, value):
        if value.lower() not in ['partial', 'complete']:
            raise AssertionError('Not a valid activation state. Should be "partial" or "complete" ')
        else:
            return value.lower()
        
    def __repr__(self):
        return (f"CatalyticTest(id={self.id!r}, zeolite={self.zeolite!r}, extrudate={self.extrudate!r}, SOD={self.state_of_deactivation!r}, deac_degree={self.deactivation_degree!r}"
               + f", tos={self.tos!r}, whsv={self.whsv!r}, catalyst_mass={self.catalyst_mass!r}, reaction_id={self.reaction_id!r}")
    
    
class CatalyticReactions(Base):
    '''
    ORM class of catalytic reactions table
    '''
    
    __tablename__ = 'catalytic_reactions'
    
    id = Column(Integer, primary_key=True)
    test_rig = Column(String)
    
    reaction = Column(String(30), unique=True)
    catalytic_tests = relationship("CatalyticTesting")
    
    reactor_internal_diameter = Column(Float)
    reactants = Column(String)
    total_pressure = Column(Float)
    reactant_partial_pressure = Column(Float)
    temperature = Column(Integer)
    activation_time = Column(Float)
    activation_atmosphere = Column(String)
    

    
    @validates('reaction', 'test_rig', 'activation_atmosphere')
    def validate_reaction(self, key, value):
        return value.upper()
    
    @validates('reactants')
    def validate_reactants(self, key, value):
        return value.lower()
    
    def __repr__(self):
        return f"CatalyticReaction(id={self.id!r}, reaction={self.test_rig}, total_pressure={self.total_pressure})"

###### CHARACTERISATION TECHNIQUES ######

# Gas Adsorption

class GasAdsorptionAnalysis(Base):
    '''
    ORM class of GasAdsorption experiments.
    '''
    
    __tablename__ = 'gas_adsorption_analysis'
    
    id = Column(Integer, primary_key=True)
    reactor_sample_id = Column(String, ForeignKey("reactor_samples.layer_code"))
    zeolite_id = Column(String, ForeignKey('zeolites.internal_id'))
    extrudate_id = Column(String, ForeignKey('extrudates.internal_id'))
    
    adsorptive = Column(String)
    measurment_temp = Column(Float)
    volume_adsorbed = Column(Float)
    sample_weight = Column(Float)

    micropore_volume = Column(Float)
    bet_area = Column(Float)
    bet_results_params = Column(JSONB)
        
    creation_date = Column(Date)
    data_loc = Column(String)   
    
    def __repr__(self):
        
        return (f"GasAnalysis(id={self.id!r}, adsorptive={self.adsorptive!r}, surface_area={self.bet_area!r}"
                + f", sample_id={self.reactor_sample_id!r}, zeolite_id={self.zeolite_id!r}, extrudate_id={self.extrudate_id!r}"
                + f", creation_date={self.creation_date!r})")
    
# tgAnalysis

class tgAnalysis(Base):
    '''
    ORM class of tgAnalysis
    
    '''
    __tablename__ = 'tg_analysis'
    
    id = Column(Integer, primary_key=True)
    reactor_sample_id = Column(String, ForeignKey("reactor_samples.layer_code"))
    zeolite_id = Column(String, ForeignKey('zeolites.internal_id'))
    extrudate_id = Column(String, ForeignKey('extrudates.internal_id'))

    water_content_wpct = Column(Float)
    meta = Column(JSONB)
    results = Column(JSONB)
    data = Column(JSONB) 

    creation_date = Column(Date, default=func.now())
    data_loc = Column(String)
    
    def __repr__(self):
        return (f"tgAnalysis(id={self.id!r}, reactor_sample_id={self.reactor_sample_id!r}"
                + f", zeolite_id={self.zeolite_id!r}, extrudate_id={self.extrudate_id!r}"
                + f", water_content={self.water_content_wpct!r}, creation_date={self.creation_date!r})")
    
# X-ray diffraction

class xrdExSituAnalysis(Base):
    
    __tablename__ = 'xrd_exsitu_analysis'
    
    id = Column(Integer, primary_key=True)
    reactor_sample_id = Column(String, ForeignKey("reactor_samples.layer_code"))
    zeolite_id = Column(String, ForeignKey('zeolites.internal_id'))
    extrudate_id = Column(String, ForeignKey('extrudates.internal_id'))

    dry_and_sealed = Column(Boolean)
    drying_temp = Column(Integer)
    nr_xrds = Column(Integer)
    xrd = Column(JSONB)
    ref_xrd = Column(JSONB)
    ref_res = Column(JSONB)
    creation_date = Column(Date)
    data_loc = Column(String)
    
    def __repr__(self):
        return (f"xrdExSituAnalysis(id={self.id!r}, reactor_sample_id={self.reactor_sample_id!r}" 
                + f", zeolite_id={self.zeolite_id!r}, extrudate_id={self.extrudate_id!r}, dry_and_sealed={self.dry_and_sealed!r}, "
                + f", drying_temp={self.drying_temp!r}, no_diff={self.nr_xrds!r}"
                + f", creation_date={self.creation_date!r})")
                
class Units(Base):

    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    table = Column(String)
    property = Column(String)
    unit = Column(String)

def create_database(user, password, host, dbname):
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(
                user,
                password,
                host,
                dbname
        )
    )
    Base.metadata.create_all(engine)
    return

def drop_database(user, password, host, dbname):
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(
                user,
                password,
                host,
                dbname
            )
        )
    Base.metadata.drop_all(engine)
    return