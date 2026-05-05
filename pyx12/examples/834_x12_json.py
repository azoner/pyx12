"""Parse 834 Benefit Enrollment & Maintenance files into JSON, emitting one
JSON document per ST transaction set with header, members, providers, and
payers flattened into a structured object."""

import collections
import glob
import json
import logging
import os.path
import sys
import tempfile

import pyx12.error_handler
import pyx12.errors
import pyx12.params
import pyx12.x12context
from pyx12.examples.jsonTable import JsonInterface


class Enrollment834Parser:
    """Import an 834 eligibility file"""

    def __init__(self, fullpath, fd_in, run_type_code="P"):
        self.logger = logging.getLogger()
        param = pyx12.params.params()
        errh = pyx12.error_handler.errh_null()
        (file_base, _ext) = os.path.splitext(os.path.basename(fullpath))
        self.outfile_base = file_base
        try:
            self.src = pyx12.x12context.X12ContextReader(param, errh, fd_in, [])
        except pyx12.errors.X12Error as e:
            err_msg = "This does not look like a X12 data file"
            self.logger.error(err_msg)
            raise pyx12.errors.X12Error(err_msg) from e

    def parse_file(self, out_dir):
        """Convert an 834 X12 file into JSON files"""
        my_count = 0
        subscribers = []
        trn_set_idx = 0
        isa = gs = st = header = None
        for datatree in self.src.iter_segments("2000"):
            if datatree.id == "2000":
                my_count += 1
                subscriber = self.get_2000(datatree, header, my_count)
                subscribers.append(subscriber)
            elif datatree.id == "ISA":
                isa = JsonInterface()
                isa.add_string("SenderCode", datatree.get_value("ISA06"))
                isa.add_string("ReceiverCode", datatree.get_value("ISA08"))
                isa.add_int("ControlNumber", datatree.get_value("ISA13"))
                isa.add_datetime(
                    "InterchangeDate",
                    "20" + datatree.get_value("ISA09"),
                    datatree.get_value("ISA10"),
                )
                isa.add_string("Version", datatree.get_value("ISA12"))
                isa.add_string("UsageIndicator", datatree.get_value("ISA15"))
                isa.seg_count = datatree.seg_count
                isa.line_number = datatree.cur_line_number
                isa.parent_line_number = None
            elif datatree.id == "IEA":
                isa = None
            elif datatree.id == "GS":
                gs = JsonInterface()
                gs.add_string("SenderCode", datatree.get_value("GS02"))
                gs.add_string("ReceiverCode", datatree.get_value("GS03"))
                gs.add_datetime(
                    "CreationDate", datatree.get_value("GS04"), datatree.get_value("GS05")
                )
                gs.add_int("GroupControlNumber", datatree.get_value("GS06"))
                gs.add_string("Version", datatree.get_value("GS08"))
                gs.seg_count = datatree.seg_count
                gs.line_number = datatree.cur_line_number
                gs.parent_line_number = isa.line_number
            elif datatree.id == "GE":
                gs = None
            elif datatree.id == "ST":
                st = JsonInterface()
                st.add_string("IdentifierCode", datatree.get_value("ST01"))
                st.add_int("ControlNumber", datatree.get_value("ST02"))
                st.add_string("ImplementationGuideVersion", datatree.get_value("ST03"))
                st.seg_count = datatree.seg_count
                st.line_number = datatree.cur_line_number
                st.parent_line_number = gs.line_number
                subscribers = []
                my_count = 0
                trn_set_idx += 1
            elif datatree.id == "SE":
                header_od = self._make_headers(isa, gs, st, header)
                _h = collections.OrderedDict()
                _h["Header"] = header_od
                _h["Members"] = subscribers
                outfile = f"{self.outfile_base}.{trn_set_idx:04d}.v1.json"
                full_outfile = os.path.join(out_dir, outfile)
                if self._write_json(_h, full_outfile):
                    self.logger.info(f"Save JSON output to {full_outfile}")
                header = None
            elif datatree.id == "BGN":
                header = JsonInterface()
                header.add_string("TransactionSetPurposeCode", datatree.get_value("BGN01"))
                header.add_string("TransactionSetReferenceNumber", datatree.get_value("BGN02"))
                header.add_datetime(
                    "TransactionSetCreationDate",
                    datatree.get_value("BGN03"),
                    datatree.get_value("BGN04"),
                )
                header.add_string("TimeZoneCode", datatree.get_value("BGN05"))
                header.add_string(
                    "OriginalTransactionSetReferenceNumber", datatree.get_value("BGN06")
                )
                header.add_string("ActionCode", datatree.get_value("BGN08"))
            elif datatree.id == "DTP":
                if datatree.get_value("DTP01") == "007":
                    header.add_string("FileEffectiveDateQualifier", datatree.get_value("DTP01"))
                    header.add_date("FileEffectiveDate", datatree.get_value("DTP[007]03"))
                elif datatree.get_value("DTP01") == "303":
                    header.add_string("FileEffectiveDateQualifier", datatree.get_value("DTP01"))
                    header.add_date("FileEffectiveDate", datatree.get_value("DTP[303]03"))
            elif datatree.id == "QTY":
                header.add_int("MemberCount", datatree.get_value("QTY[TO]02"))
            elif datatree.cur_path.find("1000A") != -1 and datatree.id == "N1":
                header.add_string("SponsorEntityIdentifierCode", datatree.get_value("N101"))
                header.add_string("SponsorName", datatree.get_value("N102"))
                header.add_string("SponsorIdentificationCodeQualifier", datatree.get_value("N103"))
                header.add_string("SponsorIdentifier", datatree.get_value("N104"))
            elif datatree.cur_path.find("1000B") != -1 and datatree.id == "N1":
                header.add_string("InsurerEntityIdentifierCode", datatree.get_value("N101"))
                header.add_string("InsurerName", datatree.get_value("N102"))
                header.add_string("InsurerIdentificationCodeQualifier", datatree.get_value("N103"))
                header.add_string("InsurerIdentificationCode", datatree.get_value("N104"))
        return True

    def get_2000(self, loop_sub, st, idx):
        "2000 Member Loop"
        sub = JsonInterface()
        sub.seg_count = loop_sub.seg_count
        sub.line_number = loop_sub.cur_line_number
        sub.parent_line_number = st.line_number

        sub.add_int("MemberOrdinal", idx)
        sub.add_string("MemberIndicator", loop_sub.get_value("INS01"))
        sub.add_string("IndividualRelationshipCode", loop_sub.get_value("INS02"))
        sub.add_string("MaintenanceTypeCode", loop_sub.get_value("INS03"))
        sub.add_string("MaintenanceReasonCode", loop_sub.get_value("INS04"))
        sub.add_string("BenefitStatusCode", loop_sub.get_value("INS05"))
        sub.add_string("MedicarePlanCode", loop_sub.get_value("INS06-1"))
        sub.add_string("MedicareEligibilityReasonCode", loop_sub.get_value("INS06-2"))
        sub.add_string("CobraQualifyingEventCode", loop_sub.get_value("INS07"))
        sub.add_string("EmploymentStatusCode", loop_sub.get_value("INS08"))
        sub.add_string("StudentStatusCode", loop_sub.get_value("INS09"))
        sub.add_string("HandicapIndicator", loop_sub.get_value("INS10"))
        sub.add_date("DateOfDeath", loop_sub.get_value("INS12"))
        sub.add_int("BirthSequenceNumber", loop_sub.get_value("INS17"))
        sub.add_string("SubscriberIdentifier", loop_sub.get_value("REF[0F]02"))
        sub.add_string("PolicyNumber", loop_sub.get_value("REF[1L]02"))
        sub.add_string("CaseNumber", loop_sub.get_value("REF[3H]02"))
        sub.add_date("EligibilityBeginDate", loop_sub.get_value("DTP[356]03"))
        sub.add_date("EligibilityEndDate", loop_sub.get_value("DTP[357]03"))
        sub.add_date("MedicaidEndDate", loop_sub.get_value("DTP[474]03"))

        sub.add_string("MemberEntityIdentifierCode", loop_sub.get_value("2100A/NM101"))
        sub.add_string("MemberLastName", loop_sub.get_value("2100A/NM103"))
        sub.add_string("MemberFirstName", loop_sub.get_value("2100A/NM104"))
        sub.add_string("MemberMiddleName", loop_sub.get_value("2100A/NM105"))
        sub.add_string("MemberNamePrefix", loop_sub.get_value("2100A/NM106"))
        sub.add_string("MemberNameSuffix", loop_sub.get_value("2100A/NM107"))
        sub.add_string("MemberIdentificationCodeQualifier", loop_sub.get_value("2100A/NM108"))
        sub.add_string("MemberIdentifier", loop_sub.get_value("2100A/NM109"))
        if loop_sub.exists("2100A/PER"):
            per = self._get_per_contact(loop_sub, "2100A")
            if "EmailAddress" in per:
                sub.add_string("MemberEmail", per["EmailAddress"])
            if "FaxNumber" in per:
                sub.add_string("MemberFaxNumber", per["FaxNumber"])
            if "TelephoneNumber" in per:
                sub.add_string("MemberTelephoneNumber", per["TelephoneNumber"])
            if "TelephoneExtension" in per:
                sub.add_string("MemberTelephoneExtension", per["TelephoneExtension"])
            if "URI" in per:
                sub.add_string("MemberURI", per["URI"])

        sub.add_string("MemberAddressLine1", loop_sub.get_value("2100A/N301"))
        sub.add_string("MemberAddressLine2", loop_sub.get_value("2100A/N302"))
        sub.add_string("MemberCity", loop_sub.get_value("2100A/N401"))
        sub.add_string("MemberState", loop_sub.get_value("2100A/N402"))
        sub.add_string("MemberZipCode", loop_sub.get_value("2100A/N403"))
        sub.add_string("MemberCountry", loop_sub.get_value("2100A/N404"))
        sub.add_string("MemberLocationQualifier", loop_sub.get_value("2100A/N405"))
        sub.add_string("MemberLocationIdentifier", loop_sub.get_value("2100A/N406"))

        sub.add_date("DateOfBirth", loop_sub.get_value("2100A/DMG02"))
        sub.add_string("Gender", loop_sub.get_value("2100A/DMG03"))
        sub.add_string("MaritalStatusCode", loop_sub.get_value("2100A/DMG04"))
        sub.add_string("EthnicityCode", loop_sub.get_value("2100A/DMG05-01"))
        sub.add_string("ClassificationOfRaceOrEthnicity", loop_sub.get_value("2100A/DMG05-02"))
        sub.add_string("RaceOrEthnicityCode", loop_sub.get_value("2100A/DMG05-03"))
        sub.add_string("CitizenshipStatusCode", loop_sub.get_value("2100A/DMG06"))

        sub.add_string("IncomeFrequencyCode", loop_sub.get_value("2100A/ICM01"))
        sub.add_number("IncomeWageAmount", loop_sub.get_value("2100A/ICM02"))
        sub.add_number("IncomeWorkHoursCount", loop_sub.get_value("2100A/ICM03"))
        sub.add_string("IncomeLocationIdentificationCode", loop_sub.get_value("2100A/ICM04"))
        sub.add_string("IncomeSalaryGradeCode", loop_sub.get_value("2100A/ICM05"))

        sub.add_string("LanguageCodeQualifier", loop_sub.get_value("2100A/LUI01"))
        sub.add_string("LanguageCode", loop_sub.get_value("2100A/LUI02"))
        sub.add_string("LanguageDescription", loop_sub.get_value("2100A/LUI03"))
        sub.add_string("LanguageUseIndicator", loop_sub.get_value("2100A/LUI04"))

        ret = sub._asdict()

        if loop_sub.exists("2100B"):
            incorrect_member_fields = self.get_incorrect_member(loop_sub.first("2100B"))
            ret["IncorrectMember"] = incorrect_member_fields

        resps = []
        for resp_loop in loop_sub.select("2100G"):
            resp_per = self.get_responsible_person(resp_loop)
            resps.append(resp_per)
        ret["ResponsiblePerson"] = resps

        coverages = []
        for loop_node in loop_sub.select("2300"):
            cov = self.get_2300(loop_node, sub)
            coverages.append(cov)
        ret["Coverages"] = coverages
        return ret

    def get_2300(self, loop_2300, parent):
        "Coverage 2300 loop"
        clsub = JsonInterface()
        clsub.seg_count = loop_2300.seg_count
        clsub.line_number = loop_2300.cur_line_number
        clsub.parent_line_number = parent.line_number

        clsub.add_string("MaintenanceTypeCode", loop_2300.get_value("HD01"))
        clsub.add_string("InsuranceLineCode", loop_2300.get_value("HD03"))
        clsub.add_string("PlanCoverageDescription", loop_2300.get_value("HD04"))
        clsub.add_string("CoverageLevelCode", loop_2300.get_value("HD05"))
        clsub.add_date("BenefitBeginDate", loop_2300.get_value("DTP[348]03"))
        clsub.add_date("BenefitEndDate", loop_2300.get_value("DTP[349]03"))
        clsub.add_date("EnrollmentSignatureDate", loop_2300.get_value("DTP[300]03"))
        clsub.add_date("MaintenanceEffectiveDate", loop_2300.get_value("DTP[303]03"))
        clsub.add_date("PremiumPaidToEndDate", loop_2300.get_value("DTP[343]03"))
        clsub.add_date("LastPremiumPaidDate", loop_2300.get_value("DTP[543]03"))

        clsub.add_string("ClientReportingCategory", loop_2300.get_value("REF[17]02"))
        ret = clsub._asdict()

        providers = []
        for loop_node in loop_2300.select("2310"):
            provider = self.get_2310_fields(loop_node)
            providers.append(provider)
        ret["Providers"] = providers

        payers = []
        idx = 0
        for loop_node in loop_2300.select("2320"):
            idx += 1
            payer_fields = self.get_2320_fields(loop_node, idx)
            payers.append(payer_fields)
        ret["Payers"] = payers
        return ret

    def get_2310_fields(self, loop):
        "Provider loop table"
        prov = JsonInterface()
        prov.seg_count = loop.seg_count
        prov.line_number = loop.cur_line_number

        prov.add_int("LineCounter", int(loop.get_value("LX01")))
        prov.add_string("EntityIdentifierCode", loop.get_value("NM101"))
        prov.add_string("EntityTypeQualifier", loop.get_value("NM102"))
        prov.add_string("LastName", loop.get_value("NM103"))
        prov.add_string("FirstName", loop.get_value("NM104"))
        prov.add_string("MiddleName", loop.get_value("NM105"))
        prov.add_string("NamePrefix", loop.get_value("NM106"))
        prov.add_string("NameSuffix", loop.get_value("NM107"))
        prov.add_string("IdentifierCodeQualifier", loop.get_value("NM108"))
        prov.add_string("IdentificationCode", loop.get_value("NM109"))
        prov.add_string("EntityRelationshipCode", loop.get_value("NM110"))
        prov.add_string("Address1", loop.get_value("N301"))
        prov.add_string("Address2", loop.get_value("N302"))
        prov.add_string("City", loop.get_value("N401"))
        prov.add_string("State", loop.get_value("N402"))
        prov.add_string("ZipCode", loop.get_value("N403"))
        prov.add_string("Country", loop.get_value("N404"))

        if loop.exists("PER"):
            per = self._get_per_contact(loop, None)
            if "EmailAddress" in per:
                prov.add_string("Email", per["EmailAddress"])
            if "FaxNumber" in per:
                prov.add_string("FaxNumber", per["FaxNumber"])
            if "TelephoneNumber" in per:
                prov.add_string("TelephoneNumber", per["TelephoneNumber"])
            if "TelephoneExtension" in per:
                prov.add_string("TelephoneExtension", per["TelephoneExtension"])
            if "URI" in per:
                prov.add_string("URI", per["URI"])

        prov.add_date("EffectiveDate", loop.get_value("PLA03"))
        prov.add_string("ChangeReason", loop.get_value("PLA04"))
        return prov._asdict()

    def get_2320_fields(self, loop, idx):
        "Payer 2320 loop"
        pay = JsonInterface()
        pay.seg_count = loop.seg_count
        pay.line_number = loop.cur_line_number

        pay.add_int("PayerOrdinal", idx)
        pay.add_string("ResponsibilitySequenceNumberCode", loop.get_value("COB01"))
        pay.add_string("MemberGroupPolicyNumber", loop.get_value("COB02"))
        pay.add_string("CoordinationOfBenefitsCode", loop.get_value("COB03"))
        pay.add_string("SocialSecurityNumber", loop.get_value("REF[SY]02"))
        pay.add_string("PolicyNumberRefZz", loop.get_value("REF[ZZ]02"))
        pay.add_string("GroupNumber", loop.get_value("REF[6P]02"))
        pay.add_string("AccountSuffixCode", loop.get_value("REF[60]02"))
        pay.add_date("CoordinationOfBenefitsBeginDate", loop.get_value("DTP[344]03"))
        pay.add_date("CoordinationOfBenefitsEndDate", loop.get_value("DTP[345]03"))
        for ins_node in loop.select("2330"):
            if ins_node.get_value("NM101") == "IN":
                pay.add_string("PayerName", ins_node.get_value("NM103"))
                if ins_node.get_value("NM108") == "FI":
                    pay.add_string("PayerFederalTaxIdNumber", ins_node.get_value("NM109"))
                if ins_node.get_value("NM108") == "XV":
                    pay.add_string("PayerPlanID", ins_node.get_value("NM109"))
                pay.add_string("PayerAddress1", ins_node.get_value("N301"))
                pay.add_string("PayerAddress2", ins_node.get_value("N302"))
                pay.add_string("PayerCity", ins_node.get_value("N401"))
                pay.add_string("PayerState", ins_node.get_value("N402"))
                pay.add_string("PayerZipCode", ins_node.get_value("N403"))
                pay.add_string("PayerCountry", ins_node.get_value("N404"))

                if ins_node.exists("PER"):
                    per = self._get_per_contact(ins_node, None)
                    if "EmailAddress" in per:
                        pay.add_string("Email", per["EmailAddress"])
                    if "FaxNumber" in per:
                        pay.add_string("FaxNumber", per["FaxNumber"])
                    if "TelephoneNumber" in per:
                        pay.add_string("TelephoneNumber", per["TelephoneNumber"])
                    if "TelephoneExtension" in per:
                        pay.add_string("TelephoneExtension", per["TelephoneExtension"])
                    if "URI" in per:
                        pay.add_string("URI", per["URI"])
                break
        return pay._asdict()

    def get_incorrect_member(self, loop_sub):
        sub = JsonInterface()
        sub.add_string("EntityIdentifierCode", loop_sub.get_value("NM101"))
        sub.add_string("EntityTypeQualifier", loop_sub.get_value("NM102"))
        sub.add_string("LastName", loop_sub.get_value("NM103"))
        sub.add_string("FirstName", loop_sub.get_value("NM104"))
        sub.add_string("MiddleName", loop_sub.get_value("NM105"))
        sub.add_string("NamePrefix", loop_sub.get_value("NM106"))
        sub.add_string("NameSuffix", loop_sub.get_value("NM107"))
        sub.add_string("IdentificationCodeQualifier", loop_sub.get_value("NM108"))
        sub.add_string("InsuredIdentifier", loop_sub.get_value("NM109"))
        if loop_sub.get_value("NM108") == "34":
            sub.add_string("SocialSecurityNumber", loop_sub.get_value("NM109"))

        sub.add_date("DateOfBirth", loop_sub.get_value("DMG02"))
        sub.add_string("Gender", loop_sub.get_value("DMG03"))
        sub.add_string("MaritalStatusCode", loop_sub.get_value("DMG04"))
        if loop_sub.get_value("DMG05-01") != "":
            sub.add_string("EthnicityCode", loop_sub.get_value("DMG05-01"))
        if loop_sub.get_value("DMG05-02") != "":
            sub.add_string("ClassificationOfRaceOrEthnicity", loop_sub.get_value("DMG05-02"))
        if loop_sub.get_value("DMG05-03") != "":
            sub.add_string("RaceOrEthnicityCode", loop_sub.get_value("DMG05-03"))
        sub.add_string("CitizenshipStatusCode", loop_sub.get_value("DMG06"))
        return sub._asdict()

    def get_responsible_person(self, loop_sub):
        sub = JsonInterface()
        sub.add_string("EntityIdentifierCode", loop_sub.get_value("NM101"))
        sub.add_string("EntityTypeQualifier", loop_sub.get_value("NM102"))
        sub.add_string("LastName", loop_sub.get_value("NM103"))
        sub.add_string("FirstName", loop_sub.get_value("NM104"))
        sub.add_string("MiddleName", loop_sub.get_value("NM105"))
        sub.add_string("NamePrefix", loop_sub.get_value("NM106"))
        sub.add_string("NameSuffix", loop_sub.get_value("NM107"))
        sub.add_string("IdentificationCodeQualifier", loop_sub.get_value("NM108"))
        sub.add_string("ResponsiblePartyIdentifier", loop_sub.get_value("NM109"))
        if loop_sub.get_value("NM108") == "34":
            sub.add_string("SocialSecurityNumber", loop_sub.get_value("NM109"))

        if loop_sub.exists("PER"):
            per = self._get_per_contact(loop_sub, None)
            if "EmailAddress" in per:
                sub.add_string("Email", per["EmailAddress"])
            if "FaxNumber" in per:
                sub.add_string("FaxNumber", per["FaxNumber"])
            if "TelephoneNumber" in per:
                sub.add_string("TelephoneNumber", per["TelephoneNumber"])
            if "TelephoneExtension" in per:
                sub.add_string("TelephoneExtension", per["TelephoneExtension"])
            if "URI" in per:
                sub.add_string("URI", per["URI"])

        sub.add_string("Address1", loop_sub.get_value("N301"))
        sub.add_string("Address2", loop_sub.get_value("N302"))
        sub.add_string("City", loop_sub.get_value("N401"))
        sub.add_string("State", loop_sub.get_value("N402"))
        sub.add_string("ZipCode", loop_sub.get_value("N403"))
        sub.add_string("Country", loop_sub.get_value("N404"))
        return sub._asdict()

    def _get_per_contact(self, per_loop, loop_id):
        "Get list of PER contact info"
        per = {}
        prefix = f"{loop_id}/PER" if loop_id is not None else "PER"
        for idx in range(1, 4):
            per_qual = per_loop.get_value(f"{prefix}0{idx * 2 + 1}")
            per_value = per_loop.get_value(f"{prefix}0{idx * 2 + 2}")
            if per_qual is not None and per_value != "":
                if per_qual == "EM":
                    per["EmailAddress"] = per_value
                elif per_qual == "FX":
                    per["FaxNumber"] = per_value
                elif per_qual == "EX":
                    per["TelephoneExtension"] = per_value
                elif per_qual == "TE":
                    per["TelephoneNumber"] = per_value
                elif per_qual == "UR":
                    per["URI"] = per_value
        return per

    def _make_headers(self, isa, gs, st, header):
        ret = collections.OrderedDict()
        for k, v in isa.fields.items():
            if not k.startswith("Interchange"):
                ret["Interchange" + k] = v["value"]
            else:
                ret[k] = v["value"]
        for k, v in gs.fields.items():
            if not k.startswith("Functional"):
                ret["Functional" + k] = v["value"]
            else:
                ret[k] = v["value"]
        for k, v in st.fields.items():
            if not k.startswith("TransactionSet"):
                ret["TransactionSet" + k] = v["value"]
            else:
                ret[k] = v["value"]
        for k, v in header.fields.items():
            ret[k] = v["value"]
        return ret

    def _write_json(self, header, outfile):
        try:
            with open(outfile, "w") as fd_final:
                fd_final.write(
                    json.dumps(header, indent=2, sort_keys=False, separators=(",", ": "))
                )
                return True
        except OSError:
            self.logger.warning(f"Failed to write {outfile}")
        return False


def parse_file(fullname, out_dir="."):
    logger = logging.getLogger()
    if not os.path.isfile(fullname):
        raise Exception(f"File {fullname} was not found")
    if not os.path.isdir(out_dir):
        logger.exception("outdir does not exist")

    with tempfile.TemporaryFile(mode="w+", encoding="ascii") as fd_src:
        with open(fullname, encoding="ascii") as fd_dx:
            fd_src.write(fd_dx.read())
        fd_src.seek(0)
        my834 = Enrollment834Parser(fullname, fd_src)
        print(fullname)
        try:
            my834.parse_file(out_dir)
        except Exception:
            logger.exception("Failed to parse file")


def main():
    """Script main program"""
    import argparse

    parser = argparse.ArgumentParser(description="834 eligibility to JSON parser")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--debug", "-d", action="store_true")
    parser.add_argument(
        "--out-dir",
        "-o",
        default=".",
        help="directory to write JSON output files (default: current directory)",
    )
    parser.add_argument("files", metavar="N", nargs="*", help="input files")
    args = parser.parse_args()

    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    stdout_hdlr = logging.StreamHandler()
    stdout_hdlr.setFormatter(formatter)
    logger.addHandler(stdout_hdlr)
    logger.setLevel(logging.INFO)

    if args.debug or args.verbose > 0:
        logger.setLevel(logging.DEBUG)

    if args.files:
        for glob_pattern in args.files:
            files = glob.glob(glob_pattern)
            print(files)
            for full_name in files:
                parse_file(full_name, args.out_dir)
    else:
        files = ["834_multiple_st_loops.txt"]
        print(files)
        for full_name in files:
            parse_file(full_name, args.out_dir)

    return True


if __name__ == "__main__":
    sys.exit(not main())
