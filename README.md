O programa exposto nesse repositório é fruto de um trabalho realizado para a disciplina de física computacional II, cursada na Universidade Federal do Rio Grande do Sul (UFRGS). Afim de exercitar os conhecimentos obtidos de simulação por métodos numéricos para resolução de equações diferenciais ordinárias.

## Introdução

A previsão do memristor por Leon Chua em 1971 representou um marco na teoria de circuitos elétricos. Baseado em argumentos de simetria matemática, Chua deduziu a existência de um quarto elemento passivo fundamental, complementando resistores, capacitores e indutores. Seu argumento baseia-se na análise das igualdades dos componentes conhecidos até então. São elas:

$$ \frac{dv}{di} = R \qquad \frac{dq}{dv} = C \qquad \frac{d\phi}{di} = L $$ 

Chua percebeu que as únicas variáveis fundamentais sem relação definida eram o fluxo magnético $\phi$ e a carga q. Assim, Chua postulou em componente que emergiria dessa situação, o \textbf{memristor}. A equação abaixo apresenta essa relação:

$$ \frac{d\phi}{dq} = M(q) $$

Sabendo que $$q = \int i\ dt\ $$ e que $$\phi = \int v\ dt\ $$, ainda podemos escrever a memristência na forma de:

$$ M(q(t)) = \frac{v(t)}{i(t)} $$

É importante frisar a diferença entre essa última equação e a definição de resistência em apresentada no início, que se dá no fato de que a resistência ser linear, tornando a tensão e a corrente dependentes entre si, enquanto o memristor é não linear, definida pelo histórico da carga (matematicamente $$q = \int i\ dt\ $$) que atravessa o componente. Justamente essa capacidade de "memorização" da passagem de carga através da alteração do seu estado de resistência que dá o nome do dispositivo.

Sua primeira realização prática ocorreu somente em 2008, por Stanley Williams e sua equipe na Hewllet-Packard (HP). A causa dessa demora é dada pelo fato do campo magnético não desempenhar um papel explícito no mecanismo de memresistência, fazendo os interessados pesquisarem nos materiais errados (STRUKOV et al., 2008; WILLIAMNS, 2008). O próprio desconhecimento desse mecanismo não era - e ainda não é - completamente compreendido. Mesmo que um resistor consiga alterar sua resistência conforme a passagem de corrente, ele precisa manter essa configuração de forma permanente até que a corrente flua novamente e haja a atualização na resistência - fenômeno conhecido como não-volatividade (VENTRA, PERSHIN, 2015).

Na pesquisa da HP foram produzidos filmes de óxido de 5nm, onde continha dióxido de titânio (TiO\textsubscript{2}) isolante e dióxido de titânio com uma ligeira depleção de átomos de oxigênio (TiO\textsubscript{2-x}) condutor, ensanduichados entre dois eletrodos de platina de 5 nm de espessura e 50 nm de largura. Esses filmes foram montados na forma de ponto cruzado (crosspoint) ilustrada na figura \subref{fig:crosspoint}, para então gerar matrizes de barras transversais (crossbar array). Na figura 2 temos uma matriz 1x17 formada desses componentes. Essa configuração é mais próxima de uma aplicação comercial, pois aumenta a densidade do componente de memória.

