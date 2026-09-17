import { configureStore, createSlice } from '@reduxjs/toolkit'

const initialForm = {
  complaint_source:'', customer_name:'', product_name:'', product_strength:'', batch_number:'', affected_quantity:'',
  manufacturing_date:'', expiry_date:'', originating_site:'', impacted_materials:'', complaint_category:'',
  complaint_description:'', defect_summary:''
}
const complaintSlice = createSlice({
  name:'complaint', initialState:{form:initialForm,risk:null,completeness:null,duplicate:null,messages:[],sourceText:'',status:'Pending Triage',savedId:null},
  reducers:{
    setAnalysis:(state, action)=>{const p=action.payload; state.form=p.complaint; state.risk=p.risk; state.completeness=p.completeness; state.duplicate=p.possible_duplicate; state.messages=p.ai_messages||[]; state.sourceText=action.meta?.sourceText||state.sourceText; state.status='Ready to Commit'},
    updateField:(state,action)=>{state.form[action.payload.key]=action.payload.value},
    setSourceText:(state,action)=>{state.sourceText=action.payload},
    setStatus:(state,action)=>{state.status=action.payload},
    setSaved:(state,action)=>{state.savedId=action.payload; state.status='Logged'},
    reset:(state)=>{Object.assign(state,{form:initialForm,risk:null,completeness:null,duplicate:null,messages:[],sourceText:'',status:'Pending Triage',savedId:null})}
  }
})
export const {setAnalysis,updateField,setSourceText,setStatus,setSaved,reset}=complaintSlice.actions
export const store=configureStore({reducer:{complaint:complaintSlice.reducer}})
