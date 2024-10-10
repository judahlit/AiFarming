

def load_data(file_path):
    fileExtension = file_path.split('.')[-1]

    if fileExtension == 'csv':
        df = pd.read_csv(file_path)
    elif fileExtension == 'xlsx' or fileExtension == 'xls':
        df = pd.read_excel(file_path)
    else:
        raise ValueError('File extension not supported: {fileExtension}'.format(fileExtension=fileExtension))

    return df