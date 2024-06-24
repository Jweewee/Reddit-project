import re
import pandas as pd

decision_making_patterns = {
    "PhysicianDecision": r"Physician making decision: ?(.+)"
}
rtpa_patterns = {
    "BodyWeight": r"Body Weight Estimated Actual\n  Kg ?(.+)",
    "IVrTPATotalDose": r"IV  rTPA  Total  Dose  ?(.+)",
    "IVrTPABolusDose": r"IV  rTPA  Bolus Dose  ?(.+)",
    "IVrTPAInfusionDose": r"IV  rTPA  Infusion Dose  ?(.+)",
    "BolusGivenTime": r"Bolus given ED (.+?)\s",
    "BolusGivenBP": r"Bolus given ED .+?\s(.+)",
    "InfusionStartedTime": r"Infusion started ED (.+?)\s",
    "InfusionStartedBP": r"Infusion started ED .+?\s(.+)",
    "CompletionLocation": r"Completion (.+?)\s",
    "CompletionTime": r"Completion .+?\s(.+)",
    "TransferredToWardBed": r"Transferred to \(Ward/Bed\) ?(.+)",
    "AdverseReaction": r"Adverse Reaction\? ?(.+)",
    "ForEndovascularTherapy": r"For Endovascular Therapy\? ?(.+)",
    "AmountOfIVTPAInfused": r"Amount of IV TPA infused: ?(.+)"
}
nihss_patterns = {
    "DateTime": r"Date / Time:  ?(.+)",
    "BloodPressure": r"Blood Pressure: ?(.+)",
    "LevelOfConsciousness": r"1a\. Level of Consciousness: ?(\d)",
    "LOCQuestions": r"1b\. LOC Questions: ?(\d)",
    "LOCCommands": r"1c\. LOC Commands: ?(\d)",
    "BestGaze": r"2\. Best Gaze: ?(\d)",
    "Visual": r"3\. Visual: ?(\d)",
    "FacialPalsy": r"4\. Facial Palsy: ?(\d)",
    "MotorArmLeft": r"5\. Motor Arm - Left: ?(\d)",
    "MotorArmRight": r"5\. Motor Arm - Right: ?(\d)",
    "MotorLegLeft": r"6\. Motor Leg - Left: ?(\d)",
    "MotorLegRight": r"6\. Motor Leg - Right: ?(\d)",
    "LimbAtaxia": r"7\. Limb ataxia: ?(\d)",
    "Sensory": r"8\. Sensory: ?(\d)",
    "BestLanguage": r"9\. Best language: ?(\d)",
    "Dysarthria": r"10 Dysarthria: ?(.+)",
    "ExtinctionAndInattention": r"11\. Extinction and Inattention: ?(\d)",
    "TotalScore": r"Total Score: ?(.+)"
}
nursing_input_patterns = {
        "ReviewingNeurologist": r"Reviewing Neurologist: ?(.*)",
        "NeurologistActivationDate": r"Neurologist Activation: Date:  ?(.+)",
        "NeurologistActivationTime": r"Time:  ?(.+hrs)",
        "NurseActivationTime": r"Nurse Activation Time:  ?(.+hrs)",
        "NurseReviewTime": r"Nurse Review Time:   ?(.+hrs)",
        "StrokeOnsetTime": r"Stroke Onset Time: (.+)",
        "PatientActivatedFrom": r"Patient Activated from: (.+)",
        "GCS_E": r"GCS: E: (\d)",
        "GCS_V": r"V: (\d)",
        "GCS_M": r"M: (\d)",
        "PowerOverRight_RUL": r"Power over Right: RUL: (\d)",
        "PowerOverRight_RLL": r"RLL: (\d)",
        "PowerOverLeft_LUL": r"Power over Left: LUL: (\d)",
        "PowerOverLeft_LLL": r"LLL: (\d)",
        "Pupils": r"Pupils: (.+)",
        "PremorbidMRS": r"Premorbid  MRS: (\d)",
        "ReasonForNoRTPA": r"Reason for NO rTPA: (.+)",
        "ReasonForNoEVT": r"Reason for NO EVT: (.+)",
        "TransferredTo": r"Transferred to: (.+)",
        "EDNurse": r"ED Nurse: ?(.*)"
    }

def extract_patterns(text, patterns):
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            extracted[key] = match.group(1)
    return extracted


all_patterns = {**nursing_input_patterns, **nihss_patterns, **rtpa_patterns, **decision_making_patterns}
# for pattern in all_patterns.values():
#     input_text = re.sub(pattern, '', input_text, flags=re.MULTILINE)


# for key in all_patterns.keys():
#     df[key] = df["Observation_value"].apply(lambda x: extract_patterns(x, all_patterns).get(key))


value = r'''
HASTEN Thrombolysis and HASTEN Endovascular\.br\\.br\Reviewing
Neurologist: Dr.Benjamin Tan\.br\Neurologist Activation: Date:
02/08/23\br\Time: 19:43 hrs\.br\Nurse Activation Time: 19:44
hrs\br\Nurse Review Time: 19:51 hrs\.br\Stroke Onset Time: 1700
hrs\br\Patient Activated from: NUH\br\GCS: E: 2\br\V: 1\br\M:
3\br\Power over Right: RUL: 3\br\RLL: 2\br\Power over Left: LUL:
1\br\LLL: 1\br\Pupils: reactive\br\Premorbid MRS: 0\.br\ED Nurse:
NA\.br\\\.br\\.br\NIHSS Assessment\.br\\.br\Date/Time:
02/08/23@1951hrs\br\rTPA Onset to Needle Duration:\br\Blood
Pressure: () 177/101\br\1a. Level of Consciousness: 1\.br\1b. LOC
Questions: 2\.br\1c. LOC Commands: 2\.br\2. Best Gaze: 2\.br\3. Visual:
21.br\4. Facial Palsy: 2\.br\5. Motor Arm- Left: 3\br\5. Motor Arm-
Right: 1\.br\6. Motor Leg - Left: 3\.br\6. Motor Leg - Right: 3\.br\7. Limb
ataxia: 0\.br\8. Sensory: 0\.br\9. Best language: 3\.br\10 Dysarthria:
2\br\11. Extinction and Inattention: 0\br\Total Score:
26\.br\\.br\\br\Body Weight Estimated\.br\ 50Kg\br\V TPA Total
Dose 30 mg (0.6mg/kg)\br\IV ITPA Bolus Dose 4.5mg\.br\IV rTPA
Infusion Dose 25.5mg\br\\br\V TPA Location Time BP
Reading\.br\Bolus given Angio suit 20:37 hrs
170/101mmhg\.br\\.br\Infusion started Angio suit 21:00
NA\br\Completion Angio suit 22:00 NA\br\Transferred to (Ward/Bed)
WD 26/15 23:00 133/36mmhg\.br\Adverse Reaction? No\.br\For
Endovascular Therapy? Yes\.br\Amount of IV TPA infused:
NA\.br\Amount of IV TPA to top up: NA Handed over to SN/SSN:
NA\br\\.br\\.br\\.br\\.br\EVT- Endovascular Therapy
WORKSHEET\.br\Hospital: NUH\.br\Neurology Consultant: Dr Benjamin
Tan\br\Interventionist: Dr Cunli\.br\Anaesthetist: Dr.Nilanthi\br\Stroke
Onset: Date: 02/08/23\.br\Time: 1700hrs\.br\EMD Arrival: Date:
02/08/01 hr Time: 1007hrel hOT Date: 02/09/2001 hr Time: 1024
hrs\.br\Angiosuite Arrival: Date: 02/08/23\.br\Time: 2032
hrs\.br\Transferred to: Ward: 26/16\br\Date: 02/08/23\.br\Time: 2300
hrs\.br\\br\EVT-Endovascular Therapy PROCEDURE DETAILS\.br\Groin
Puncture Time: 2106 hrs\.br\Recanalization Time: 2225 hrs\.br\IA rTPA
used? If so, state dosage: Yes 3mg\.br\Anaesthesia: General
Anaesthesia\.br\Device Used: Solitire/Trevo NXT/Pneumbra
suction\.br\Baseline TICI Score (Dr to advise): 0\.br\Post EVT TICI Score
(Dr to advise): 2B\.br\Any Complications? (Dr to advise):
No\.br\\\br\\.br\Blood Pressure Monitoring Chart\.br\Time Vital Signs
(BP/HR)\.br\If Applicable Medications Dosage Remarks\.br\(If
any)\.br\2034hrs 170/101 GTN Patch 10mg Applied in angio
suit\.br\2045hrs 208/117 IV Labetalol 15mg Given in angio
suit\.br\\.br\Taken over case from SSN Khiu in ED.\.br\\br\Initially
planned for EVT as patient's family reported that patient had
been\.br\compliant with Apixaban, however, upon clarification with
patient's daughter,\.br\patient had ran out of apixaban for the last 2
days, and was not taking it.\.br\On the way to angio suit Dr. Benjamin
decided to give IV rTPA Dose calculated\.br\together with SSN Khiu in
angio suit.\.br\After given bolus dose noted pt's BP high 208/117.IV
Labetalol 15 mg served\.br\Decision made by Dr.Benjamin to intubate pt
and start infusion. Infusion started\.br\during EVT so unable to get
BP\br\\\.br\Case handed over to SN Hong Ming.\.br\\.br\Monitoring of
vitals:\br\15 mts x 2hrs followed by 30 mts x 6 hrs then
hourly\.br\\.br\Post Removal Femoral Sheath Care:\.br\1) Monitor
puncture site for hematoma/bleeding hourly for 8 hours.
Manual\.br\compression if necessary.\.br\2) Monitor pulse, BP every
15min for 1hour, every 30min for next 3hrs and 1\.br\hourly for
subsequent 4 hours\.br\3) Rest in bed x 6-8 hours\.br\\.br\\.br\ 
'''

value2 = """Date / Time: 2024-06-06 08:30
Blood Pressure: () 177/101
1a. Level of Consciousness: 2
1b. LOC Questions: 1
1c. LOC Commands: 1
2. Best Gaze: 0
3. Visual: 2
4. Facial Palsy: 1
5. Motor Arm - Left: 2
5. Motor Arm - Right: 2
6. Motor Leg - Left: 1
6. Motor Leg - Right: 1
7. Limb ataxia: 0
8. Sensory: 2
9. Best language: 1
10 Dysarthria: 2
11. Extinction and Inattention: 0
Total Score: 10"""

print(extract_patterns(value, nursing_input_patterns))
a = extract_patterns(value, nursing_input_patterns)
print(extract_patterns(value2, nihss_patterns))
print(extract_patterns(value, rtpa_patterns))
print(extract_patterns(value, decision_making_patterns))

dfs = {}
dfs["NursingInput"] = pd.DataFrame([a] )
# print(dfs["NursingInput"].to_string()   )