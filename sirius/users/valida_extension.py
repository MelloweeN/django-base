from django.core.exceptions import ValidationError
 
def valid_extension_image(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.jpg')):
 
        raise ValidationError("Archivos permitidos: .jpg, .jpeg, .png, .gif, .bmp")

def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and 
        not value.name.endswith('.gif') and
        not value.name.endswith('.jpg') and

        not value.name.endswith('.doc') and
        not value.name.endswith('.docx') and
        not value.name.endswith('.xls') and
        not value.name.endswith('.xlsx') and
        not value.name.endswith('.ppt') and
        not value.name.endswith('.pptx') and
    	
        not value.name.endswith('.pdf') and
        not value.name.endswith('.zip') and
        not value.name.endswith('.rar') and
    	not value.name.endswith('.txt')):
 
        raise ValidationError("Archivos permitidos: .jpg, .jpeg, .png, .gif, Suite Office, .pdf, .zip, .rar, .txt")