import json
import re
from datetime import datetime

class QualityPlanGenerator:
    def __init__(self, db_path="normes_db.json"):
        with open(db_path, 'r', encoding='utf-8') as f:
            self.db = json.load(f)
        self.materials = self.db['materials']
        self.ndt_reqs = self.db['ndt_requirements']
    
    def identify_material(self, grade_text):
        grade_text = grade_text.upper()
        for material in self.materials:
            for grade in material['grades']:
                if grade.upper() in grade_text:
                    return material
        return self.materials[0]
    
    def extract_psl(self, text):
        match = re.search(r'PSL[-\s]*(\d)', text, re.IGNORECASE)
        return match.group(1) if match else "1"
    
    def extract_standards(self, text):
        standards = []
        for std in ["API 6A", "API 5CT", "API 7-1"]:
            if std in text.upper():
                standards.append(std)
        return standards if standards else ["API 6A"]
    
    def generate_operations(self, of_data):
        material = self.identify_material(of_data['grade'])
        standards = self.extract_standards(of_data['raw_text'])
        psl = self.extract_psl(of_data['raw_text'])
        
        ops = []
        ops.append({
            "op": "01", "description": "Receiving Material check", "interne": "X", "tierce": "",
            "document": "FO-02-PRO",
            "criteria": f"Chemical composition: {material['chemical_composition']}. Certificat EN 10204 Type 3.1.",
            "signature": "", "record": "Manifest", "comment": ""
        })
        ops.append({
            "op": "05", "description": "Visual & Dimensional Inspection after cutting", "interne": "X", "tierce": "",
            "document": "FO-51-PRO",
            "criteria": f"Dimensions per drawing, tolerances per {', '.join(standards)} PSL{psl}.",
            "signature": "", "record": "FO-51-PRO", "comment": ""
        })
        # NDT
        ndt_list = []
        for std in standards:
            if std in self.ndt_reqs:
                ndt_list.extend(self.ndt_reqs[std].values())
        ndt_text = ", ".join(set(ndt_list)) if ndt_list else "MPI, PT"
        ops.append({
            "op": "13", "description": "NDT", "interne": "", "tierce": "X",
            "document": "PR-13-PRO",
            "criteria": f"Per {', '.join(standards)} PSL{psl} : {ndt_text}",
            "signature": "Gaith Elleuch", "record": "NDT Report", "comment": ""
        })
        # Final control
        mech = material['mechanical_properties']
        mech_crit = f"UTS ≥ {mech['UTS_min_MPa']}MPa, YS ≥ {mech['YS_min_MPa']}MPa, Elongation ≥ {mech['elongation_min']}%"
        ops.append({
            "op": "17", "description": "Final control", "interne": "X", "tierce": "",
            "document": "FO-19-PRO",
            "criteria": mech_crit + ". Marquage complet.",
            "signature": "Kais Hmidet, Ahmed Drira", "record": "FO-19-PRO", "comment": "Received/Finished"
        })
        return ops, material
    
    def parse_of_file(self, content):
        text = content.upper()
        data = {
            'raw_text': text,
            'customer': re.search(r'CUSTOMER[:\s]*(\w+)', text).group(1) if re.search(r'CUSTOMER[:\s]*(\w+)', text) else '',
            'order_no': re.search(r'ORDER[:\s]*N[O°]?[:\s]*([A-Z0-9-]+)', text).group(1) if re.search(r'ORDER[:\s]*N[O°]?[:\s]*([A-Z0-9-]+)', text) else '',
            'wo_no': re.search(r'WO[:\s]*([A-Z0-9-]+)', text).group(1) if re.search(r'WO[:\s]*([A-Z0-9-]+)', text) else '',
            'product': re.search(r'(ADAPTER|FLANGE|CONNECTOR)[^.]*', text).group(0) if re.search(r'(ADAPTER|FLANGE|CONNECTOR)[^.]*', text) else '',
            'grade': re.search(r'GRADE[:\s]*([A-Z0-9\s-]+)', text).group(1).strip() if re.search(r'GRADE[:\s]*([A-Z0-9\s-]+)', text) else '',
            'date': datetime.now().strftime("%d/%m/%Y")
        }
        return data
