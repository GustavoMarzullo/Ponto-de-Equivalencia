#importando as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def diff2(dataframe,x,y):
    '''Retorna a derivada d2y/dx2 de tal dataframe.\nx e y são as colunas do dataframe a serem derivadas.'''
    pontos=[0,0]
    for i in range(2,len(dataframe[x])):
        try:
            delta1=(dataframe[y][i-1]-dataframe[y][i-2])/(dataframe[x][i-1]-dataframe[x][i-2])
            delta2=(dataframe[y][i]-dataframe[y][i-1])/(dataframe[x][i]-dataframe[x][i-1])
            pontos.append((delta2-delta1)/(dataframe[x][i]-dataframe[x][i-2]))
        except IndexError:
            continue
    return pontos

def pe(dataframe,n_pontos,plotar=False,filtro=False):
    '''Retorna o ponto de equivalência da titulação (Vtit e pH). O dataframe deve conter uma coluna com 'pH' e outra com 'Vtit'.'''
    assert n_pontos==1 or n_pontos== 2 or n_pontos== 3,('Máximo de 3 pontos')

    dataframe=dataframe[['pH','Vtit']] #tirando as colunas vazias (frescura)
    dataframe=dataframe.assign(diff2=diff2(dataframe,'Vtit','pH')) #adiciona uma coluna com a segunda derivada
    
    if n_pontos==1:
        y0=dataframe.loc[dataframe['diff2'] == dataframe['diff2'].max()]['diff2'].values[0] #isso tudo é para fazer uma reta entre os pontos de máximo e mínimo da segunda derivada
        x0=dataframe.loc[dataframe['diff2'] == dataframe['diff2'].max()]['Vtit'].values[0]
        y1=dataframe.loc[dataframe['diff2'] == dataframe['diff2'].min()]['diff2'].values[0]
        x1=dataframe.loc[dataframe['diff2'] == dataframe['diff2'].min()]['Vtit'].values[0]
        b=(x1*y0-x0*y1)/(x1-x0) #y=ax+b
        a=(y1-y0)/(x1-x0)
        
        Vtit=-b/a #raiz da equação diff2(Vtit)=a*Vtit+b
        
        y0=dataframe.loc[dataframe['diff2'] == dataframe['diff2'].max()]['pH'].values[0] #mudando o eixo y de d2pH/dVtit2 para pH
        y1=dataframe.loc[dataframe['diff2'] == dataframe['diff2'].min()]['pH'].values[0]
        b=(x1*y0-x0*y1)/(x1-x0) #redefinindo os valores de a e b
        a=(y1-y0)/(x1-x0)
        
        pH=a*Vtit + b #aqui está se calculando o pH de equivalência
        
        print('Vtit='+str(round(Vtit,2))+'\npH='+str(round(pH,2)))
        if plotar==True:
            fig, axs = plt.subplots(2)
            axs[0].plot(dataframe['Vtit'],dataframe['pH'],color='black',linewidth=1)
            axs[0].set(xlabel='Vtit',ylabel='pH ')
            axs[1].plot(dataframe['Vtit'],dataframe['diff2'],color='black',linewidth=1)
            axs[1].set(xlabel='Vtit',ylabel='d2pH/dVtit2')
            plt.show()
    else:
        #fazendo o clustering
        km=KMeans(n_clusters=n_pontos)
        diff_pred=km.fit_predict(dataframe[['pH','Vtit']])
        dataframe['Cluster']=diff_pred
        
        if n_pontos==2: 
            df1=dataframe[dataframe.Cluster==0]
            df2=dataframe[dataframe.Cluster==1]
            
            #achando o pH1 e Vtit1
            y0=df1.loc[df1['diff2'] == df1['diff2'].max()]['diff2'].values[0] 
            x0=df1.loc[df1['diff2'] == df1['diff2'].max()]['Vtit'].values[0]
            y1=df1.loc[df1['diff2'] == df1['diff2'].min()]['diff2'].values[0]
            x1=df1.loc[df1['diff2'] == df1['diff2'].min()]['Vtit'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0) 
            a=(y1-y0)/(x1-x0)
            
            Vtit1=-b/a 
            
            y0=df1.loc[df1['diff2'] == df1['diff2'].max()]['pH'].values[0] 
            y1=df1.loc[df1['diff2'] == df1['diff2'].min()]['pH'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0)
            a=(y1-y0)/(x1-x0)
            
            pH1=a*Vtit1 + b 
            
            #achando o pH2 e Vtit2
            y0=df2.loc[df2['diff2'] == df2['diff2'].max()]['diff2'].values[0] 
            x0=df2.loc[df2['diff2'] == df2['diff2'].max()]['Vtit'].values[0]
            y1=df2.loc[df2['diff2'] == df2['diff2'].min()]['diff2'].values[0]
            x1=df2.loc[df2['diff2'] == df2['diff2'].min()]['Vtit'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0) 
            a=(y1-y0)/(x1-x0)
            
            Vtit2=-b/a 
            
            y0=df2.loc[df2['diff2'] == df2['diff2'].max()]['pH'].values[0] 
            y1=df2.loc[df2['diff2'] == df2['diff2'].min()]['pH'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0)
            a=(y1-y0)/(x1-x0)
            
            pH2=a*Vtit2 + b 
        
            print('PE 1:'+'\nVtit='+str(round(Vtit1,2))+'\npH='+str(round(pH1,2)))
            print('\nPE 2:'+'\nVtit='+str(round(Vtit2,2))+'\npH='+str(round(pH2,2)))
            if plotar==True:
                fig, axs = plt.subplots(2)
                axs[0].plot(dataframe['Vtit'],dataframe['pH'],color='black',linewidth=1)
                axs[0].set(xlabel='Vtit',ylabel='pH')
                axs[1].plot(df1['Vtit'],df1['diff2'],color='red',linewidth=1)
                axs[1].plot(df2['Vtit'],df2['diff2'],color='black',linewidth=1)
                axs[1].set(xlabel='Vtit',ylabel='d2pH/dVtit2')
                plt.show()
            
        else:
            df1=dataframe[dataframe.Cluster==0]
            df2=dataframe[dataframe.Cluster==1]
            df3=dataframe[dataframe.Cluster==2]
            
            #achando o pH1 e Vtit1
            y0=df1.loc[df1['diff2'] == df1['diff2'].max()]['diff2'].values[0] 
            x0=df1.loc[df1['diff2'] == df1['diff2'].max()]['Vtit'].values[0]
            y1=df1.loc[df1['diff2'] == df1['diff2'].min()]['diff2'].values[0]
            x1=df1.loc[df1['diff2'] == df1['diff2'].min()]['Vtit'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0) 
            a=(y1-y0)/(x1-x0)
            
            Vtit1=-b/a 
            
            y0=df1.loc[df1['diff2'] == df1['diff2'].max()]['pH'].values[0] 
            y1=df1.loc[df1['diff2'] == df1['diff2'].min()]['pH'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0)
            a=(y1-y0)/(x1-x0)
            
            pH1=a*Vtit1 + b 
            
            #achando o pH2 e Vtit2
            y0=df2.loc[df2['diff2'] == df2['diff2'].max()]['diff2'].values[0] 
            x0=df2.loc[df2['diff2'] == df2['diff2'].max()]['Vtit'].values[0]
            y1=df2.loc[df2['diff2'] == df2['diff2'].min()]['diff2'].values[0]
            x1=df2.loc[df2['diff2'] == df2['diff2'].min()]['Vtit'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0) 
            a=(y1-y0)/(x1-x0)
            
            Vtit2=-b/a 
            
            y0=df2.loc[df2['diff2'] == df2['diff2'].max()]['pH'].values[0] 
            y1=df2.loc[df2['diff2'] == df2['diff2'].min()]['pH'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0)
            a=(y1-y0)/(x1-x0)
            
            pH2=a*Vtit2 + b 
            
            #achando o pH3 e Vtit3
            y0=df3.loc[df3['diff2'] == df3['diff2'].max()]['diff2'].values[0] 
            x0=df3.loc[df3['diff2'] == df3['diff2'].max()]['Vtit'].values[0]
            y1=df3.loc[df3['diff2'] == df3['diff2'].min()]['diff2'].values[0]
            x1=df3.loc[df3['diff2'] == df3['diff2'].min()]['Vtit'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0) 
            a=(y1-y0)/(x1-x0)
            
            Vtit3=-b/a 
            
            y0=df3.loc[df3['diff2'] == df3['diff2'].max()]['pH'].values[0] 
            y1=df3.loc[df3['diff2'] == df3['diff2'].min()]['pH'].values[0]
            b=(x1*y0-x0*y1)/(x1-x0)
            a=(y1-y0)/(x1-x0)
            
            pH3=a*Vtit3 + b 
        
            print('PE 1:'+'\nVtit='+str(round(Vtit1,2))+'\npH='+str(round(pH1,2)))
            print('\nPE 2:'+'\nVtit='+str(round(Vtit2,2))+'\npH='+str(round(pH2,2)))
            print('\nPE 3:'+'\nVtit='+str(round(Vtit3,2))+'\npH='+str(round(pH3,2)))
            if plotar==True:
                fig, axs = plt.subplots(2)
                axs[0].plot(dataframe['Vtit'],dataframe['pH'],color='black',linewidth=1)
                axs[0].set(xlabel='Vtit',ylabel='pH')
                axs[1].plot(df1['Vtit'],df1['diff2'],color='red',linewidth=1)
                axs[1].plot(df2['Vtit'],df2['diff2'],color='black',linewidth=1)
                axs[1].plot(df3['Vtit'],df3['diff2'],color='green',linewidth=1)              
                axs[1].set(xlabel='Vtit',ylabel='d2pH/dVtit2')
                plt.show()

