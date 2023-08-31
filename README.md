
# MercVisionIQ


Este projeto consiste numa aplicação de redes neuronais convolucionais para a classificação dos modelos das viaturas Mercedes Benz e smart, seguida da identificação de cores através do algoritmo de agrupamento K-means.


## Requerimentos
Qualquer IDE python3, Anaconda Jupyter Notebook (opcional)

- Processamento de dados em Python 3.
    Pandas, Numpy, Matplotlib
- Algoritmos Machine Learning.
    Scikit-Learn, SciPy
- Algoritmos Deep Learning usados pelo Python.
    TensorFlow, Keras, Scikit-Learn, Pandas, Matplotlib, NumPy
- Tkinter, pyforms para formulário

## Otimização GPU
O objetivo do uso da GPU é acelerar o treino da CNN. Para tal foi necessário segui o tutorial
- https://www.tensorflow.org/install/pip?hl=pt-br
## Dataset usado
Para treino e teste da rede neuronal foram usadas 26319 imagens de treino e 169 de teste de viaturas pertencentes a 23 classes(modelos). 
!ATENÇÃO! É necessário que as viaturas estejam organizadas em pastas com o respetivo modelo, uma vez que cada modelo corresponde a uma classe.

Enquanto que para o treino tende-se a dar preferência a imagens cuidadas, para o teste queremos imagens próximas da realidade para obtermos uma precisão de classificação realista.

De modo a colocar as imagens de treino numa lista, para cada modelo, fazemos:

```bash
  dir = '.'
  Citan_train=dir + "/MODELOS_treino/Citan/"
  train_Citan = [(dir + "/MODELOS_treino/Citan/{}").format(i) for i in os.listdir(Citan_train)]
  ....
```
No diretório de treino, as imagens devem estar dividas por modelos, tendo cada um destes +- o mesmo número de imagens, para equilibrar o modelo. Neste caso, cada modelo tem por volta de 1000 imagens. O script abaixo aproveita um csv do CarBase e coloca os modelos numa lista.
```bash
import xlwings as xw
wb = xw.Book('../CarBase - MO.xlsx')
sht = wb.sheets['Sheet1']
modelos = sht.range('E3:E652').value
modelos_unique= []
for i in modelos:
    if i not in modelos_unique:
        modelos_unique.append(i)
```
Apartir de imagens de cada viatura divididas por matrículas. Conseguimos associar a matrícula ao modelo e copiar a imagem para a respetiva pasta do modelo.
```bash
dict1 = dict(zip(matriculas,modelos))
for matricula in dict1.keys():
    newpath = r'.\FOTOS\{}'.format(matricula) 
    if os.path.isdir('./FOTOS/{}'.format(matricula)):
        i=0
        try:
            for i in range(1,4):
                file = './FOTOS/{}/00{}.jpg'.format(matricula,i)
                dst = ".MODELOS2_treino/{}".format(dict1[matricula])
                shutil.copy(file, dst)
                os.rename("./MODELOS2_treino/{}/00{}.jpg".format(dict1[matricula],i),"C:/Users/jgoncalves/Desktop/MODELOS2/{}/00{}.jpg".format(dict1[matricula],k))
                print(i,file)
                k+=1
        except:
            continue
```
## Aumento de dados
Uma vez que as imagens inicialmente disponibilizadas não são suficientes para alimentar o modelo em causa, há a necessidade de aumentarmos estes dados através de transformações. Para modelos imagens suficientes, não foi necessário aplicar transformações.

As transformações usadas foram: 
- rotação,
- reflexão horizontal,
- filtros de sharpness,
- contraste
- cor.

Os scripts foram disponibilizados. ATENÇÃO: as transformações foram aplicadas com prudência, uma vez que as imagens têm de manter o realismo.

## Rede Neuronal
Após redimensionamento das imagens para 256x256 (através de cv2.resize) e escaladas para [0,1], iniciou-se o treino da rede neuronal. !DICAS! usar camadas de normalização (batch normalization) e usar pooling layers depois de camadas convolucionais. Quanto maior o número de filtros, mais parâmetros são processados e mais features são detetadas, mas mais 'pesado' fica o treino.
```bash
model = keras.Sequential(
        [
        keras.Input(shape=input_shape),
        layers.ZeroPadding2D(padding=(1, 1)),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu",padding='same'),
        layers.ZeroPadding2D(padding=(3, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.BatchNormalization(),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu",padding='same'),
        layers.ZeroPadding2D(padding=(3, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(128, activation='relu'),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu",padding='same'),
        layers.ZeroPadding2D(padding=(3, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu",padding='same'),
        layers.ZeroPadding2D(padding=(3, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)), 
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu",padding='same'),
        layers.ZeroPadding2D(padding=(3, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)), 
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu",padding='same'),
        layers.ZeroPadding2D(padding=(3, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)), 
        layers.Flatten(),
        layers.Dense(200),
        layers.Dropout(0.2),
        layers.Dense(100),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax"),
    ]
)
```
| Rede            |                                                 |
| ----------------- | ---------------------------------------------------------------- |
| Otimizador     | SGD (lr=0.01) |
| loss function       | categorical_crossentropy |
| batch size       | 16 |
| epochs     | 20|

Os seguintes comandos guardam e carregam a configuração do modelo (pessos adotados) de forma a não ser necessário o treino e a classificação seja instantânea.
```bash
model.save("./modelo_cnn_modelos/marca_modelo_sgd5.h5")
model = tf.keras.models.load_model("./modelo_cnn_modelos/marca_modelo_sgd3.h5")
```

## Transfer Learning
O algoritmo marcas-sgd3_tfl é semelhante ao algoritmo marcas_sgd3, contudo utilizar um modelo de rede neuronal diferente. De modo a poupar tempo e recursos no treino da rede neuronal, pode-se utilizar uma versão de modelo CNN de classificação convencional tal como o AlexNet, Inception, ResNet, já treinado numa base de dados que faça sentido (ex. ImageNet). Desta forma, abdica-se de treinar o modelo, colocando umas camadas 'header' de compatibilidade, podendo obter-se uma precisão razoável ( o que não foi o caso ). Colocando ainda as camadas para não treinar.
```bash
for layer in baseModel.layers:
    layer.trainable=False
print("[INFO] compiling model...")
```

## Resultados
São dados em percentagem, quanto mais próximo do 1 melhor. É importante ter em atenção a precisão de treino, mas a de teste é mais importante. Neste caso, em 169 imagens classificou corretamente 88%.
| Rede            |                                                 |
| ----------------- | ---------------------------------------------------------------- |
| Perdas     | 0.82 |
| Precisão       | 0.88 |

## Possíveis limitações
Overfitting - o modelo fica muito dependente dos dados de treino e não consegue classificar corretamente dados não vistos ( imagens que não fazem parte do dataset treino). Causas possíveis: poucos dados de treino, uso de loss function não adequado, modelo muito complexo. Para detetar este fenómeno, estar atento ao valor da loss function ( = cost function) e se este se mantiver constante pode ser devido ao overfitting.

O uso de redes neuronais é um processo de aprendizagem supervisionado ( 'supervised'), o que significa que é necessário que os dados tenham 'label'.

## Reconhecimento de Cor
O reconhecimento de cor recorre ao algoritmo de agrupamento K-means com 3 clusters e está inserido no script que corre o formulário de interface. Por outro lado, este processo é não supervisionado. No script 'forms':
## Requerimentos
Além dos anteriores:
```bash
import pyforms
from pyforms import BaseWidget
from pyforms.controls import ControlText, ControlButton
from tkinter import *
from tkinter.filedialog import askopenfilename,askdirectory
from sklearn.cluster import KMeans
import webcolors
import PIL
from PIL import Image, ImageTk
```
## Possíveis melhorias
- Mostrar imagem que se quer classificar no formulário
 

Mais informações sobre K-means: https://towardsdatascience.com/k-means-clustering-algorithm-applications-evaluation-methods-and-drawbacks-aa03e644b48a
