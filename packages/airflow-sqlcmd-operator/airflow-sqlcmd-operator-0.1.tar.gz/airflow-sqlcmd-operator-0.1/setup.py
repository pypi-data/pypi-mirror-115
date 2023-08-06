from distutils.core import setup
setup(
    name = 'airflow-sqlcmd-operator',         
    packages = ['airflow_sqlcmd_operator'],   
    version = '0.1',      
    license='MIT',        
    description = 'Custom Airflow BashOperator for Microsoft sqlcmd',   
    author = 'Rodrigo Dewes',                   
    author_email = 'rdewes@gmail.com',      
    url = 'https://github.com/dewes/airflow-sqlcmd-operator',   
    download_url = 'https://github.com/dewes/airflow-sqlcmd-operator/archive/refs/tags/v_01.tar.gz',    # I explain this later on
    keywords = ['Airflow', 'operator', 'SQLServer', 'sqlcmd'],   
    install_requires=[
            'apache-airflow',            
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    ],
)