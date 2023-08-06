import streamlit as st
from compartmentModel import compartmentModel
import time
import json
import pandas



#KNOWN BUGS:
#If you open/close the sidebar, it wont auto collapse/expand until a sidebar item is used that performs that function
#There isn't a catch/recovery state if things break currently. Tons of saftey nets, but if you break something it will need to restart


state = st.session_state
if 'sidebarExpansion' not in state:
    state['sidebarExpansion'] = 'collapsed'
#DONE: add model to session state 
if 'model' not in state:
    state['model'] = compartmentModel()
if 'importFlag' not in state:
    state['importFlag'] = False
if 'prevKey' not in state:
    state['prevKey'] = None
if 'compFlag' not in state:
    state['compFlag'] = False
if 'prevCompKey' not in state:
    state['prevCompKey'] = None
    
def expand_sidebar():
    state['sidebarExpansion'] = 'expanded'
def collapse_sidebar():
    state['sidebarExpansion'] = 'collapsed'


st.set_page_config(page_title='Compartmental Modeling', page_icon=None, layout="centered", initial_sidebar_state=state['sidebarExpansion'], menu_items=None)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.title('Compartmental Modeling Software')
#SIDEBAR ======================================================================================
#DONE: integrate with backend
#Import Container ---------------------------------------------------------------------------
importExpander = st.sidebar.expander('Import Model')
if(state.get(state['prevKey']) is not None):
    state['importFlag'] = True
randKey = 'importUploader'+time.strftime("%Y%m%d-%H%M%S")
if(state['importFlag'] == False):
    state['prevKey'] = randKey
importData = importExpander.file_uploader('Choose a .JSON model', type=['json'], key=randKey)
if state['importFlag'] == True:
    state['model'].load_from_json(jsonObject = json.load(state.get(state['prevKey'])))
    state['prevKey'] = None
    state['importFlag'] = False
    state['model'].run()
    st.experimental_rerun()

#Export Container ----------------------------------------------------------------------------
exportExpander = st.sidebar.expander('Export Model')
exportExpander.download_button(
    label="Download model as .JSON",
    data=state['model'].create_json(),
    file_name='CompartmentModel' + time.strftime("%Y%m%d-%H%M%S") + '.json')

#Comparison Container ------------------------------------------------------------------------
comparisonExpander = st.sidebar.expander('Import Comparison Data')
if(state.get(state['prevCompKey']) is not None):
    state['compFlag'] = True
compKey = 'compUploader'+time.strftime("%Y%m%d-%H%M%S")
if(state['compFlag'] == False):
    state['prevCompKey'] = compKey
compData = comparisonExpander.file_uploader('Choose a .CSV file', type=['csv'], key=compKey)
if state['compFlag'] == True:
    state['model'].import_comparison_data_from_obj(state.get(state['prevCompKey']))
    state['prevCompKey'] = None
    state['compFlag'] = False
    st.experimental_rerun()

#Run Button --------------------------------------------------------------------------------
if(st.sidebar.button('Run Model')):
    state['model'].run()
    st.experimental_rerun()
st.sidebar.markdown("""---""")


#Main Page Tabs____________________________________________________________________
#____________________________________________________________________________________
#DONE: add support for multiple optimization methods
dataTab, optTab, visTab = st.tabs(['Data', 'Optimization', 'Visualization'])

#tmax interface ----------------------------------------------------------------------------
#tmax interface tabs
tmaxColumns = dataTab.columns(4)
tmaxColumns[0].write('Tmax: ' + str(state['model'].get_tmax()))
tmaxField = tmaxColumns[1].text_input('tmaxField', label_visibility='collapsed', value=state['model'].get_tmax())
if(tmaxColumns[2].button('Update Tmax', key='tmaxButton')):
    state['model'].update_tmax(tmaxField)
    st.experimental_rerun()

#Data Tabs==========================================================================================
compartmentTab, parameterTab, linkageTab = dataTab.tabs(['Compartments', 'Parameters', 'Linkages'])

#region Compartments Tab----------------------------------------------------------------------------------------
#DONE: integrate compartment df backend
compartmentTab.dataframe(state['model'].get_initCompartments_df(), use_container_width=True, height=350)
compColumns = compartmentTab.columns(10)
if(compColumns[0].button('Add', key='button1', on_click=expand_sidebar) or state.get('FormSubmitter:form1-Submit')): 
    if state['button1']:
        temp = st.sidebar.form(key='form1')
        temp.write('Add Compartment')
        compName = temp.text_input('Compartment Name: ', key='compName')
        compVal = temp.text_input('Initial Value: ', key='compVal')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form1-Submit']:
        #DONE: integrate add compartment backend
        state['model'].add_compartment(state['compName'], state['compVal'])
        st.experimental_rerun()

if(compColumns[1].button('Edit', key='button2', on_click=expand_sidebar) or state.get('FormSubmitter:form2-Submit')):
    if state['button2']:
        temp = st.sidebar.form(key='form2')
        #DONE: integrate compartment name backend
        temp.write('Edit Compartment: ')
        compName = temp.selectbox('Compartment Name:', state['model'].get_compartment_names(), key='compName')
        compVal = temp.text_input('Initial Value:', key='compVal')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form2-Submit']:
        #DONE: integrate edit compartment backend
        state['model'].edit_compartment(state['compName'], state['compVal'])
        st.experimental_rerun()

if(compColumns[2].button('Delete', key='button3', on_click=expand_sidebar) or state.get('FormSubmitter:form3-Submit')):
    if state['button3']:
        temp = st.sidebar.form(key='form3')
        #DONE: integrate compartment name backend
        temp.write('Delete Compartment:')
        compName = temp.selectbox('Compartment Name:', state['model'].get_compartment_names(), key='compName')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form3-Submit']:
        #DONE: integrate del compartment backend
        state['model'].del_compartment(state['compName'])
        st.experimental_rerun()
#endregion

#region Parameters Tab-------------------------------------------------------------------------------------------
#DONE: integrate parameter df backend
parameterTab.dataframe(state['model'].get_parameterValues_df(), use_container_width=True, height=350)
paramColumns = parameterTab.columns(6)
if(paramColumns[0].button('Add Parameter', key='button4', on_click=expand_sidebar) or state.get('FormSubmitter:form4-Submit')):
    if state['button4']:
        temp = st.sidebar.form(key='form4')
        temp.write('Add Parameter')
        paramName = temp.text_input('Parameter Name: ', key='paramName')
        paramVal = temp.text_input('Initial Value: ', key='paramVal')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form4-Submit']:
        #DONE: integrate add parameter backend
        state['model'].add_parameter(state['paramName'], state['paramVal'])
        st.experimental_rerun()

if(paramColumns[1].button('Edit Parameter', key='button5', on_click=expand_sidebar) or state.get('FormSubmitter:form5-Submit')):
    if state['button5']:
        temp = st.sidebar.form(key='form5')
        temp.write('Edit Parameter')
        #DONE integrate parameter name backend
        paramName = temp.selectbox('Parameter Name: ', state['model'].get_parameter_names(), key='paramName')
        paramValue = temp.text_input('Initial Value: ', key='paramVal')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form5-Submit']:
        #DONE: integrate add parameter backend
        state['model'].edit_parameter(state['paramName'], state['paramVal'])
        st.experimental_rerun()

if(paramColumns[2].button('Delete Parameter', key='button6', on_click=expand_sidebar) or state.get('FormSubmitter:form6-Submit')):
    if state['button6']:
        temp = st.sidebar.form(key='form6')
        temp.write('Delete Parameter')
        #DONE integrate parameter name backend
        paramName = temp.selectbox('Parameter Name: ', state['model'].get_parameter_names(), key='paramName')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form6-Submit']:
        #DONE: integrate delete parameter backend
        state['model'].del_parameter(state['paramName'])
        st.experimental_rerun()

if(paramColumns[3].button('Add Parameter Change', key='button7', on_click=expand_sidebar) or state.get('FormSubmitter:form7-Submit')):
    if state['button7']:
        temp = st.sidebar.form(key='form7')
        temp.write('Add Parameter Change')
        #DONE integrate parameter name backend
        paramName = temp.selectbox('Parameter Name: ', state['model'].get_parameter_names(), key='paramName')
        paramVal = temp.text_input('New Value: ', key='paramVal')
        #DONE: add tmax note to field name
        paramDate = temp.text_input('Change Date: (0 - ' + str(state['model'].get_tmax()-1) + ')', key='paramDate')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form7-Submit']:
        #DONE: integrate add parameter change backend
        state['model'].add_parameter_change(state['paramName'], state['paramVal'], state['paramDate'])
        st.experimental_rerun()

if(paramColumns[4].button('Edit Parameter Change', key='button8', on_click=expand_sidebar) or state.get('FormSubmitter:form8-Submit')):
    if state['button8']:
        temp = st.sidebar.form(key='form8')
        temp.write('Edit Parameter Change')
        #DONE integrate parameter list backend
        paramName = temp.selectbox('Parameter Change: ', state['model'].get_parameter_changes(), key='paramName')
        paramVal = temp.text_input('New Value: ', key='paramVal')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form8-Submit']:
        #DONE: integrate edit parameter change backend
        state['model'].add_parameter_change(state['paramName'][0], state['paramVal'], state['paramName'][2])
        st.experimental_rerun()

if(paramColumns[5].button('Delete Parameter Change', key='button9', on_click=expand_sidebar) or state.get('FormSubmitter:form9-Submit')):
    if state['button9']:
        temp = st.sidebar.form(key='form9')
        temp.write('Delete Parameter Change')
        #DONE integrate parameter list backend
        compName = temp.selectbox('Parameter Change: ', state['model'].get_parameter_changes(), key='paramName')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form9-Submit']:
        #DONE: integrate delete parameter change backend
        state['model'].del_parameter_change(state['paramName'][0], state['paramName'][2])
        st.experimental_rerun()
#endregion

#region Linkages Tab----------------------------------------------------------------------------------------------------
#DONE: integrate linkages df backend
linkageTab.dataframe(state['model'].get_linkage_df(), use_container_width=True, height=350)
linkColumns = linkageTab.columns(10)
if(linkColumns[0].button('Add', key='button10', on_click=expand_sidebar) or state.get('FormSubmitter:form10-Submit')): 
    if state['button10']:
        temp = st.sidebar.form(key='form10')
        temp.write('Add Linkage')
        fromName = temp.selectbox('From Compartment: ', state['model'].get_compartment_names(), key='fromName')
        toName = temp.selectbox('To Compartment: ', state['model'].get_compartment_names(), key='toName')
        formula = temp.text_input('Link Formula: ', key='formula')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form10-Submit']:
        #DONE: integrate add linkage backend
        state['model'].add_linkage(state['fromName'], state['toName'], state['formula'])
        st.experimental_rerun()

if(linkColumns[1].button('Edit', key='button11', on_click=expand_sidebar) or state.get('FormSubmitter:form11-Submit')):
    if state['button11']:
        temp = st.sidebar.form(key='form11')
        temp.write('Edit Linkage')
        #DONE integrate parameter name backend
        linkName = temp.selectbox('From/To Compartments Name: ', state['model'].get_linkage_names(), key='linkName')
        linkFormula = temp.text_input('New Formula: ', key='formula')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form11-Submit']:
        #DONE: integrate edit linkage backend
        state['model'].edit_linkage(state['linkName'][0], state['linkName'][1], state['formula'])
        st.experimental_rerun()

if(linkColumns[2].button('Delete', key='button12', on_click=expand_sidebar) or state.get('FormSubmitter:form12-Submit')):
    if state['button12']:
        temp = st.sidebar.form(key='form12')
        temp.write('Delete Linkage')
        #DONE integrate link name backend
        linkName = temp.selectbox('From/To Compartments Name: ', state['model'].get_linkage_names(), key='linkName')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form12-Submit']:
        #DONE: integrate delete linkage backend
        state['model'].del_linkage(state['linkName'][0], state['linkName'][1])
        st.experimental_rerun()

#endregion

#region Data display -----------------------------------------------------------------------------------------------
dataTab.markdown("""---""")
#Comparison Data
dataTabCols = dataTab.columns(3)
dataTabCols[0].write('Model Data')
dataTabCols[2].download_button(
    label="Download data as .CSV",
    data=str(state['model'].create_csv_string()),
    file_name='CompartmentModel' + time.strftime("%Y%m%d-%H%M%S") + '.csv')


#DONE: integrate model data chart backend
dataTab.dataframe(state['model'].get_compartments_df(), use_container_width=True)

#Comparison Data
#DONE: integrate comparison data chart backend
dataTab.write('Comparison Data')
dataTab.dataframe(state['model'].get_comparison_data(), use_container_width=True)

#endregion

#region OPTIMIZATION TAB=====================================================================================
optMethod = optTab.selectbox('Optimization Method', ['Genetic Algorithm', 'Linear Regression (NYI)'])
if(optMethod == 'Genetic Algorithm'):
    # predicted, observed, numGenerations, numChromosomes, mutationChance
    predicted = optTab.selectbox('Predicting Variable: ', options=state['model'].get_compartment_names())
    observed = optTab.selectbox('Observed Variable: ', options=list(state['model'].get_comparison_data().keys()))
    excluded = optTab.multiselect('Parameters to exclude from GA: ', options=state['model'].get_parameter_names())
    numGens = optTab.number_input('Number of Generations:', value=100)
    numChroms = optTab.number_input('Number of Chromosomes:', value=100)
    mutChance = optTab.number_input('Chance of Random Mutation:', value=0.1)
    genePercent = optTab.number_input('Percent of time point containing change:',value = 0.20, min_value = 0.0, max_value = 1.0)
    confirmationBox = optTab.checkbox('I understand that this will overwrite the current model.')

    if(optTab.button('Run Genetic Algorithm') and confirmationBox):
        with st.spinner('Performing genetic algorithm...'):
            finalModel = state['model'].genetic_algorithm(predicted, observed, excluded, numGens, numChroms, mutChance, genePercent)[0]
            state['model'].set_parameter_changes(finalModel)
            state['model'].run()
            st.experimental_rerun()
        

if(optMethod == 'Linear Regression (NYI)'):
    optTab.write('UNDER CONSTRUCTION')

#endregion

#region VIS TABS===================================================================================================

def visualizeSuite(container, predicted, observed):
    predDf = state['model'].get_compartment_as_df(predicted)
    obsDf = state['model'].get_comparison_as_df(observed)
    predDelta = state['model'].get_compartment_delta_as_df(predicted)
    obsDelta = state['model'].get_comparison_delta_as_df(observed)
    RMSE = state['model'].RMSE_independent(predDf, obsDf)
    delta_RMSE = state['model'].RMSE_independent(predDelta, obsDelta)
    RMSEovertime = state['model'].RMSE_independent_overtime(predDf, obsDf)
    deltaRMSEovertime = state['model'].RMSE_independent_overtime(predDelta, obsDelta)

    container.write('predicted.' + predicted + ' / observed.' + observed + ': RMSE = ' + str(RMSE))
    container.line_chart(predDf.join(obsDf))
    container.write('predicted.' + predicted + ' / observed.' + observed + ' RMSE over time')
    container.line_chart({'RMSE from t=0 to t': RMSEovertime})
    container.write('predicted.' + predicted + ' delta / observed.' + observed + ' delta: RMSE = ' + str(delta_RMSE))
    container.line_chart(predDelta.join(obsDelta))
    container.write('predicted.' + predicted + ' delta / observed.' + observed + ' delta RMSE over time')
    container.line_chart({'RMSE from t=0 to t': deltaRMSEovertime})
compsToVis = visTab.multiselect('Compartments to show: ', options=state['model'].get_compartment_names())
if compsToVis:
    compDfs = [state['model'].get_compartment_as_df(comp) for comp in compsToVis]
    temp = pandas.concat(compDfs, axis=1)
    print(temp)
    visTab.line_chart(temp)

visTab.markdown("""---""")

if(visTab.button('Pair Variables', key='button13', on_click=expand_sidebar) or state.get('FormSubmitter:form13-Submit')): 
    if state['button13']:
        temp = st.sidebar.form(key='form13')
        temp.write('Pair Variables For Visualization')
        predName = temp.selectbox('Predicted Variable Name: ', options=state['model'].get_compartment_names(), key='predName')
        obsName = temp.selectbox('Observed Variable Name: ', options=state['model'].get_comparison_data().keys(), key='obsName')
        submitted = temp.form_submit_button('Submit', on_click=collapse_sidebar)
    if state['FormSubmitter:form13-Submit']:
        visualizeSuite(visTab, state['predName'], state['obsName'])

#endregion