import requests
from fpdf import FPDF
from PIL import Image
import io
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

# NetBox API URL und Token
NETBOX_URL = os.getenv("NETBOX_URL")
NETBOX_TOKEN = os.getenv("NETBOX_TOKEN")
TENANT_ID = os.getenv("TENANT_ID")

# API-Header
headers = {
    'Authorization': f'Token {NETBOX_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


# Funktion, um die Daten eines Tenants abzurufen
def get_tenant_data(tenant_id):
    response = requests.get(f'{NETBOX_URL}tenancy/tenants/{tenant_id}/', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Fehler beim Abrufen der Tenant-Daten: {response.status_code} [get_tenant_data(tenant_id), {tenant_id}]')
        return None


# Funktion, um die Locations eines Tenants abzurufen
def get_tenant_locations(tenant_id):
    response = requests.get(f'{NETBOX_URL}dcim/sites/?tenant_id={tenant_id}', headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Fehler beim Abrufen der Standort-Daten: {response.status_code} [get_tenant_locations(tenant_id), {tenant_id}]')
        return None


# Funktion, um die Racks einer Location abzurufen
def get_location_racks(location_id):
    response = requests.get(f'{NETBOX_URL}dcim/racks/?site_id={location_id}', headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Fehler beim Abrufen der Rack-Daten: {response.status_code} [get_location_racks(location_id), {location_id}]')
        return None


# Funktion, um die Devices eines Racks abzurufen
def get_rack_devices(rack_id):
    response = requests.get(f'{NETBOX_URL}dcim/devices/?rack_id={rack_id}', headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Fehler beim Abrufen der Geräte-Daten: {response.status_code} [get_rack_devices(rack_id), {rack_id}]')
        return None


# Funktion, um die Interfaces eines Geräts abzurufen
def get_device_interfaces(device_id):
    response = requests.get(f'{NETBOX_URL}dcim/interfaces/?device_id={device_id}', headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Fehler beim Abrufen der Schnittstellen-Daten: {response.status_code} [get_device_interfaces(device_id), {device_id}]')
        return None


# Funktion, um die Front Ports eines Geräts abzurufen
def get_device_frontports(device_id):
    response = requests.get(f'{NETBOX_URL}dcim/front-ports/?device_id={device_id}', headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Fehler beim Abrufen der Schnittstellen-Daten: {response.status_code} [get_device_frontports(device_id), {device_id}]')
        return None


# Funktion, um die Rear Ports eines Geräts abzurufen
def get_device_rearports(device_id):
    response = requests.get(f'{NETBOX_URL}dcim/rear-ports/?device_id={device_id}', headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f'Fehler beim Abrufen der Schnittstellen-Daten: {response.status_code} [get_device_rearports(device_id), {device_id}]')
        return None


# Funktion, um Kabelverbindungen eines Interfaces abzurufen
def get_cable_details(cable_id):
    response = requests.get(f'{NETBOX_URL}dcim/cables/{cable_id}/', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Fehler beim Abrufen der Schnittstellen-Daten: {response.status_code} [get_cable_details(cable_id), {cable_id}]')
        return None


# Funktion, um die Bilddaten herunterzuladen und als Image-Objekt zu konvertieren
def get_image_from_url(url):
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        print(f'Fehler beim Abrufen des Bildes: {response.status_code} [get_image_from_url(url), {url}]')
        return None


# Funktion, um die Daten in eine PDF zu exportieren
def export_to_pdf(tenant_data, locations):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Tenant-Informationen zur PDF hinzufügen
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Tenant Information", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {tenant_data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Slug: {tenant_data['slug']}", ln=True)
    pdf.cell(200, 10, txt=f"Description: {tenant_data['description']}", ln=True)
    pdf.ln(10)

    for location in locations:
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt=f"Location: {location['name']}", ln=True, align='C')
        pdf.ln(5)

        racks = get_location_racks(location['id'])
        for rack in racks:
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt=f"Rack: {rack['name']}", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Facility ID: {rack['facility_id']}", ln=True)
            pdf.cell(200, 10, txt=f"Type: {rack['type']['label'] if rack['type'] else 'N/A'}", ln=True)
            pdf.cell(200, 10, txt=f"Width: {rack['width']}", ln=True)
            pdf.cell(200, 10, txt=f"Height: {rack['u_height']} U", ln=True)
            pdf.cell(200, 10, txt=f"Status: {rack['status']['label']}", ln=True)
            pdf.cell(200, 10, txt=f"Serial Number: {rack['serial']}", ln=True)
            pdf.cell(200, 10, txt=f"Asset Tag: {rack['asset_tag']}", ln=True)
            pdf.cell(200, 10, txt=f"Role: {rack['role']['name'] if rack['role'] else 'N/A'}", ln=True)
            pdf.cell(200, 10, txt=f"Comments: {rack['comments']}", ln=True)
            pdf.ln(10)


            devices = get_rack_devices(rack['id'])
            for device in devices:
                pdf.add_page()
                pdf.set_font("Arial", size=14)
                pdf.cell(200, 10, txt=f"Device Name: {device['name']}", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Device Type: {device['device_type']['model']}", ln=True)
                pdf.cell(200, 10, txt=f"Device Role: {device['device_role']['name']}", ln=True)
                pdf.cell(200, 10, txt=f"Serial Number: {device['serial']}", ln=True)
                pdf.cell(200, 10, txt=f"Site: {device['site']['name']}", ln=True)
                pdf.ln(5)

                frontports = get_device_frontports(device['id'])
                rearports = get_device_rearports(device['id'])
                if device['device_role']['name'] == "Patchpanel":
                    pdf.cell(200, 10, txt="Front-Ports:", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(30, 10, txt="Name", border=1)
                    pdf.cell(40, 10, txt="Type", border=1)
                    pdf.cell(50, 10, txt="Connected To", border=1)
                    pdf.cell(35, 10, txt="Cable Type", border=1)
                    pdf.cell(15, 10, txt="Length", border=1)
                    pdf.cell(20, 10, txt="Color", border=1)
                    pdf.ln(10)
                    for interface in frontports:
                        pdf.cell(30, 5, txt=interface['name'], border=1)
                        pdf.cell(40, 5, txt=interface['type']['label'], border=1)
                        if interface['cable']:
                            cable = get_cable_details(interface['cable']['id'])
                            if cable and cable['a_terminations']:
                                connected_to = cable['a_terminations'][0]['object']['device']['name'] + " - " + \
                                               cable['a_terminations'][0]['object']['device']['display']
                                pdf.cell(50, 5, txt=connected_to, border=1)
                                pdf.cell(35, 5, txt=cable['type'], border=1)
                                length = cable['length'] if cable['length'] else 'N/A'
                                length_unit = cable['length_unit']['value'] if cable['length_unit'] else 'N/A'
                                pdf.cell(15, 5, txt=str(length) + ' ' + str(length_unit), border=1)
                                pdf.cell(20, 5, txt=cable['color'], border=1)
                            else:
                                pdf.cell(50, 5, txt="N/A", border=1)
                                pdf.cell(35, 5, txt="N/A", border=1)
                                pdf.cell(15, 5, txt="N/A", border=1)
                                pdf.cell(20, 5, txt="N/A", border=1)
                        else:
                            pdf.cell(50, 5, txt="N/A", border=1)
                            pdf.cell(35, 5, txt="N/A", border=1)
                            pdf.cell(15, 5, txt="N/A", border=1)
                            pdf.cell(20, 5, txt="N/A", border=1)
                        pdf.ln(5)
                    pdf.ln(2.5)

                    pdf.cell(200, 10, txt="Rear-Ports:", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(30, 10, txt="Name", border=1)
                    pdf.cell(40, 10, txt="Type", border=1)
                    pdf.cell(50, 10, txt="Connected To", border=1)
                    pdf.cell(35, 10, txt="Cable Type", border=1)
                    pdf.cell(15, 10, txt="Length", border=1)
                    pdf.cell(20, 10, txt="Color", border=1)
                    pdf.ln(10)
                    for interface in rearports:
                        pdf.cell(30, 5, txt=interface['name'], border=1)
                        pdf.cell(40, 5, txt=interface['type']['label'], border=1)
                        if interface['cable']:
                            cable = get_cable_details(interface['cable']['id'])
                            if cable and cable['a_terminations']:
                                connected_to = cable['a_terminations'][0]['object']['device']['name'] + " - " + \
                                               cable['a_terminations'][0]['object']['device']['display']
                                pdf.cell(50, 5, txt=connected_to, border=1)
                                pdf.cell(35, 5, txt=cable['type'], border=1)
                                length = cable['length'] if cable['length'] else 'N/A'
                                length_unit = cable['length_unit']['value'] if cable['length_unit'] else 'N/A'
                                pdf.cell(15, 5, txt=str(length) + ' ' + str(length_unit), border=1)
                                pdf.cell(20, 5, txt=cable['color'], border=1)
                            else:
                                pdf.cell(50, 5, txt="N/A", border=1)
                                pdf.cell(35, 5, txt="N/A", border=1)
                                pdf.cell(15, 5, txt="N/A", border=1)
                                pdf.cell(20, 5, txt="N/A", border=1)
                        else:
                            pdf.cell(50, 5, txt="N/A", border=1)
                            pdf.cell(35, 5, txt="N/A", border=1)
                            pdf.cell(15, 5, txt="N/A", border=1)
                            pdf.cell(20, 5, txt="N/A", border=1)
                        pdf.ln(5)
                    pdf.ln(2.5)


                interfaces = get_device_interfaces(device['id'])
                if interfaces:
                    pdf.cell(200, 5, txt="Interfaces:", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(30, 5, txt="Name", border=1)
                    pdf.cell(40, 5, txt="Type", border=1)
                    pdf.cell(50, 5, txt="Connected To", border=1)
                    pdf.cell(35, 5, txt="Cable Type", border=1)
                    pdf.cell(15, 5, txt="Length", border=1)
                    pdf.cell(20, 5, txt="Color", border=1)
                    pdf.ln(5)
                    for interface in interfaces:
                        pdf.cell(30, 5, txt=interface['name'], border=1)
                        pdf.cell(40, 5, txt=interface['type']['label'], border=1)
                        if interface['cable']:
                            cable = get_cable_details(interface['cable']['id'])
                            if cable and cable['a_terminations']:
                                connected_to = cable['a_terminations'][0]['object']['device']['name'] + " - " + \
                                               cable['a_terminations'][0]['object']['device']['display']
                                pdf.cell(50, 5, txt=connected_to, border=1)
                                pdf.cell(35, 5, txt=cable['type'], border=1)
                                length = cable['length'] if cable['length'] else 'N/A'
                                length_unit = cable['length_unit']['value'] if cable['length_unit'] else 'N/A'
                                pdf.cell(15, 5, txt=str(length) + ' ' + str(length_unit), border=1)
                                pdf.cell(20, 5, txt=cable['color'], border=1)
                            else:
                                pdf.cell(50, 5, txt="N/A", border=1)
                                pdf.cell(35, 5, txt="N/A", border=1)
                                pdf.cell(15, 5, txt="N/A", border=1)
                                pdf.cell(20, 5, txt="N/A", border=1)
                        else:
                            pdf.cell(50, 5, txt="N/A", border=1)
                            pdf.cell(35, 5, txt="N/A", border=1)
                            pdf.cell(15, 5, txt="N/A", border=1)
                            pdf.cell(20, 5, txt="N/A", border=1)
                        pdf.ln(5)
                    pdf.ln(2.5)

                if 'custom_fields' in device:
                    pdf.cell(200, 10, txt="Custom Fields:", ln=True)
                    for field, value in device['custom_fields'].items():
                        pdf.cell(200, 10, txt=f" - {field}: {value}", ln=True)
                    pdf.ln(5)

                if 'rack' in device and device['rack']:
                    pdf.cell(200, 10, txt=f"Rack Position: {device['position']}", ln=True)
                    pdf.ln(5)

    # PDF speichern mit Tenant-Namen und Zeitstempel
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_filename = f"{tenant_data['name']}_{timestamp}.pdf"
    pdf.output(pdf_filename)
    print(f"PDF wurde erfolgreich als '{pdf_filename}' erstellt.")


# Main-Funktion
if __name__ == "__main__":
    tenant_data = get_tenant_data(TENANT_ID)
    locations = get_tenant_locations(TENANT_ID)
    if tenant_data and locations is not None:
        export_to_pdf(tenant_data, locations)
