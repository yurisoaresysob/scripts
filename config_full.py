import re, subprocess, socket, openpyxl, shutil, os

while True:
    os.system('clear')
    entrada_inicial = input('''-------------------------
|*** Seja Bem-vindo! ***|
-------------------------
O que deseja configurar?

1 - Configurações iniciais
2 - Arquivos de configuração do asterisk
3 - Auto-provisionamento

Opção: ''')

    if entrada_inicial == '1':
        print('Ainda não é uma opção válida.\n')
        input('Pressione qualquer tecla para continuar...')
        os.system('clear')
        continue
        
        # 1 - Criação dos usuários
        # 2 - 

    elif entrada_inicial == '2':

        # Version 1.4 (01-07-2024)
        #============ Definindo funções =============================
        #--> Substituição
        def replace_pat(filename, pattern, replacement):
           with open(filename, 'r') as file:
               text = file.read()


           text = re.sub(pattern, replacement, text)


           with open(filename, 'w') as file:
               file.write(text)

        #--> Escrita como apêndice
        def writing_n(filename, text):
           with open(filename, 'a') as file:
               file.write('\n')
               file.write(text)

        #--> Escrita para arquivos criados
        def writing(filename, text):
           with open(filename, 'a') as file:
               file.write(text)

        # --> Executar comandos no Shell       
        def shell(command):
           subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        # --> Substituir linha inteira
        def replace_line(arquivo, padrao, substituicao):
           with open(arquivo, 'r') as f:
               linhas = f.readlines()


           with open(arquivo, 'w') as f:
               for linha in linhas:
                   if re.search(padrao, linha):
                       f.write(substituicao + '\n')
                   else:
                       f.write(linha)

        # --> Criar padrão de digitos no extensions.ramais
        def digit_process(dig1, dig2):
            check_num = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
            num1 = set()
            num2 = set()
            num3 = set()
            num4 = set()
            cont = 0
            final_loop = None
            ramal = '_'

        #----- Tratamento Dígito 1 -------

            cont = 0 
            for i in range(dig1, dig2, 1):
                cont += 1 
                i = str(i)
                num1.add(i[0])
                if check_num == num1:
                    ramal += 'X'
                    final_loop = None
                    break
                elif cont == 10000:
                    ramal += f'[{str(dig1)[0]}-{str(dig2)[0]}]'
                    final_loop = None
                    break
                final_loop = True

            if final_loop == True: 
                if str(dig1)[0] != str(dig2)[0]:
                    ramal += f'[{str(dig1)[0]}-{str(dig2)[0]}]'
                else:
                    ramal += str(dig1)[0]


        # ---- Tratamento Dígito 2 -------

            cont = 0 
            for i in range(dig1, dig2, 1):
                cont += 1 
                i = str(i)
                num2.add(i[1])
                if check_num == num2:
                    ramal += 'X'
                    final_loop = None
                    break
                elif cont == 1000:
                    ramal += f'[{str(dig1)[1]}-{str(dig2)[1]}]'
                    final_loop = None
                    break
                final_loop = True

            if final_loop == True: 
                if str(dig1)[1] != str(dig2)[1]:
                    ramal += f'[{str(dig1)[1]}-{str(dig2)[1]}]'
                else:
                    ramal += str(dig1)[1]

        # ---- Tratamento Dígito 3 -------
            cont = 0
            for i in range(dig1, dig2, 1):
                cont += 1 
                i = str(i)
                num3.add(i[2])
                if check_num == num3:
                    ramal += 'X'
                    final_loop = None
                    break
                elif cont == 100:
                    ramal += f'[{str(dig1)[2]}-{str(dig2)[2]}]'
                    final_loop = None
                    break
                final_loop = True

            if final_loop == True: 
                if str(dig1)[2] != str(dig2)[2]:
                    ramal += f'[{str(dig1)[2]}-{str(dig2)[2]}]'
                else:
                    ramal += str(dig1)[2]


        # ---- Tratamento Dígito 4 -------
            for i in range(dig1, dig2, 1):
                cont += 1 
                i = str(i)
                num4.add(i[3])
                if check_num == num4:
                    ramal += 'X'
                    final_loop = None
                    break
                elif cont == 10:
                    if str(dig1)[3] != str(dig2)[3]:
                        ramal += f'[{str(dig1)[3]}-{str(dig2)[3]}]'
                    else:
                        ramal += str(dig1)[3]
                    final_loop = None
                    break
                final_loop = True
            if final_loop == True: 
                if str(dig1)[3] != str(dig2)[3]:
                    ramal += f'[{str(dig1)[3]}-{str(dig2)[3]}]'
                else:
                    ramal += str(dig1)[3]
            return ramal


        # --> Textos para configuração
        #------pjsip.conf
        pjsip_padrao = '''[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0


;============== Inclusão dos ramais
#include <pjsip.ramais>


;============== Inclusão dos Troncos


#include <pjsip.transito>
'''

        #-----pjsip.ramais
        pjsip_ramais = ''';================ Templates

[endpoint](!)
type=endpoint
context=ramais
disallow=all
allow=opus
allow=g722
allow=alaw
allow=h264
language=pt_BR


[auth](!)
type=auth
auth_type=userpass
password=%PASS%


[aor](!)
type=aor
max_contacts=2
qualify_frequency=300
        '''

        # ---- Criação dos ramais
        create_ramais = '''[%NUM%](endpoint)
auth=%NUM%
aors=%NUM%
call_group =
pickup_group =


[%NUM%](auth)
username=%NUM%


[%NUM%](aor)
'''

        #----pjsip.transito
        pjsip_transito = ''';=============== Tronco com Transito CINDACTA 1

[c1transito]
type=aor
contact=sip:10.227.11.222:5060
qualify_frequency=300


[c1transito]
type=endpoint
context=ramais
disallow=all
allow=opus
allow=alaw
aors=c1transito
direct_media=no


[c1transito]
type=identify
endpoint=c1transito
match=10.227.11.222


;=============== Tronco com Transito PAME-RJ


[pametransito]
type=aor
contact=sip:10.40.165.222:5060
qualify_frequency=300


[pametransito]
type=endpoint
context=ramais
disallow=all
allow=opus
allow=alaw
aors=pametransito
direct_media=no


[pametransito]
type=identify
endpoint=pametransito
match=10.40.165.222
        '''

        #----- pjsip.rte1
        pjsip_gwe1 = ''';============== Tronco com Gateway E1

[gwe1]
type=aor
contact=sip:%IP_GATE%:5060
qualify_frequency=300


[gwe1]
type=endpoint
context=ramais
disallow=all
allow=alaw
allow=ulaw
aors=gwe1


[gwe1]
type=identify
endpoint=gwe1
match=%IP_GATE%
        '''

        #-----pjsip.pstn
        pjsip_pstn = ''';============== Tronco com Operadora

[pstn]
type=aor
contact=sip:%IP_OPERADORA%:5060
qualify_frequency=300


[pstn]
type=endpoint
context=ramais
disallow=all
allow=alaw
allow=ulaw
aors=pstn


[pstn]
type=identify
endpoint=pstn
match=%IP_OPERADORA%
        '''

        #-----extensions.conf
        extensions_conf = '''[ramais]

#include <extensions.padrao>


#include <extensions.ramais>
        '''

        #-----extensions.padrao
        extensions_padrao = ''';========================= DIALPLAN PADRÃO


;!!!! Adicionar CONTEXTO "[ramais]" em linha anterior


;#include <extensions.padrao>


;========== LIGAÇÕES LOCAIS FIXO




exten => _0ZXXXXXXX,1,Set(CALLERID(ALL)=%PREFIX_OM%${CALLERID(num)})
exten => _0ZXXXXXXX,2,dial(pjsip/0%DDD_OM%${EXTEN:1}@c1transito)
exten => _0ZXXXXXXX,3,dial(pjsip/0%DDD_OM%${EXTEN:1}@pametransito)
exten => _0ZXXXXXXX,4,dial(pjsip/0${EXTEN:1}@%TRUNK%)




;========== LIGAÇÕES LOCAIS MÓVEL


exten => _0ZXXXXXXXX,1,Set(CALLERID(ALL)=%PREFIX_OM%${CALLERID(num)})
exten => _0ZXXXXXXXX,2,dial(pjsip/0${EXTEN:1}@%TRUNK%)


;========== LIGAÇÕES DDD


exten => _00Z.,1,Set(CALLERID(ALL)=0%DDD_OM%%PREFIX_OM%${CALLERID(num)})
exten => _00Z.,2,dial(pjsip/${EXTEN:1}@c1transito)
exten => _00Z.,3,dial(pjsip/${EXTEN:1}@pametransito)
exten => _00Z.,4,dial(pjsip/00%PREFIX_OPERADORA%${EXTEN:2}@%TRUNK%)


;========== LIGAÇÕES DDI


exten => _000X.,1,dial(pjsip/00%PREFIX_OPERADORA%${EXTEN:3}@%TRUNK%)


;========== LIGAÇÕES EMERGENCIAIS


exten => _01XX,1,dial(pjsip/${EXTEN:1}@%TRUNK%)


;========== LIGAÇÕES 0800


exten => _00800X.,1,dial(pjsip/${EXTEN:1}@%TRUNK%)


;========== LIGAÇÕES DE UTILIDADE ESPECÍFICA


exten => _01XXXX,1,dial(pjsip/${EXTEN:1}@%TRUNK%)


;==================== Pickup - Captura de chamada direta


exten => _**XXXX,1,Pickup(${EXTEN:2})
        '''

        #-------features.conf
        features_conf = '''[general]

        featuredigittimeout = 5000
        transferdigittimeout = 5
        pickupexten = **


[featuremap]


        blindxfer = #
        disconnect = *0
        atxfer = *#
        '''

        #------extensions.ramais
        extensions_ramais = ''';----------------Ramais DDR--------------------------------------------------------------------

exten => %PADRAO_RAMAIS%,1,NoOp(Ramal ${CALLERID(num)} LIGANDO PARA ${EXTEN})
 same => n,NoOp(Verificando BlackList para ${CALLERID(num)})
 same => n,Set(Bloqueado=${SHELL(cat /etc/asterisk/blacklist | grep -c "${CALLERID(num)}")})
 same => n,GotoIf($[${Bloqueado} = 1]?Bloqueado:noBloqueado)
 same => n(noBloqueado),dial(${PJSIP_DIAL_CONTACTS(${EXTEN})},60,tT)
 same => n,Hangup()
 same => n(Bloqueado),Playback(ext-disabled)
 same => n,Hangup()
'''

        # --> Iniciando script (BANNER)
        os.system('clear')
        banner = (r'''               
                              .$$$$$$$$$$$$$$$=..      
                           .$7$7..          .7$$7:.    
                         .$$:.                 ,$7.7   
                       .$7.     7$$$$           .$$77  
                    ..$$.       $$$$$            .$$$7 
                   ..7$   .?.   $$$$$   .?.       7$$$.
                  $.$.   .$$$7. $$$$7 .7$$$.      .$$$.
                .777.   .$$$$$$77$$$77$$$$$7.      $$$,
                $$$~      .7$$$$$$$$$$$$$7.       .$$$.
               .$$7          .7$$$$$$$7:          ?$$$.
               $$$          ?7$$$$$$$$$$I        .$$$7 
               $$$       .7$$$$$$$$$$$$$$$$      :$$$. 
               $$$       $$$$$$7$$$$$$$$$$$$    .$$$.  
               $$$        $$$   7$$$7  .$$$    .$$$.   
               $$$$             $$$$7         .$$$.    
               7$$$7            7$$$$        7$$$      
                $$$$$                        $$$       
                 $$$$7.                       $$       
                  $$$$$$$.           .7$$$$$$  $$      
                    $$$$$$$$$$$$7$$$$$$$$$.$$$$$$      
                      $$$$$$$$$$$$$$$$.                

//////////////////////////////////////////////////////////////////////////
//                                                                      //
//                                                                      //
//     ________   __ ______  ___  ___  ___ _____      ______   ___      //
//     | ___ \ \ / / | ___ \/ _ \ |  \/  ||  ___|     | ___ \ |_  |     //
//     | |_/ /\ V /  | |_/ / /_\ \| .  . || |__ ______| |_/ /   | |     //
//     | ___ \ \ /   |  __/|  _  || |\/| ||  __|______|    /    | |     //
//     | |_/ / | |   | |   | | | || |  | || |___      | |\ \/\__/ /     //
//     \____/  \_/   \_|   \_| |_/\_|  |_/\____/      \_| \_\____/      //
//                                                                      //
//                                                                      //
//////////////////////////////////////////////////////////////////////////
        ''')
        print(banner)

        #================ Variáveis ====================================
        # --> Declaração de variáveis
        first_range = None
        last_range = None
        header_pjsip = None
        ip_dns = 'Nenhum'
        ip_ntp = 'Nenhum'

        # --> Entrada de dados
        hostname = input('\nQual o Hostname pretende atribuir à máquina? ')
        os.system('clear')

        while True:
            print(banner)
            config_ntp_dns = input('O que pretende configurar?\n1 - NTP\n2 - DNS\n3 - NTP e DNS\nOpção: ')
            if config_ntp_dns == '1':
                ip_ntp = input('Qual o IP do NTP? ')
                break
            elif config_ntp_dns == '2':
                ip_dns = input('Qual o IP do DNS? ')
                break
            elif config_ntp_dns == '3':
                ip_ntp = input('Qual o IP do NTP? ')
                ip_dns = input('Qual o IP do DNS? ')
                break
            else:
                input('\nErro: Opção inválida\nPressione "Enter" para tentar novamente...')
                continue
        os.system('clear')

        print(banner)
        pass_reg = input('Qual a senha para registro de telefones? ')
        os.system('clear')

        print(banner)
        trunk_pstn = input('''O que deseja configurar como tronco com a operadora?
        Digite o Número correspondente à opção:
        1- E1  
        2- SIP Trunk                  

        Opção: ''')
        os.system('clear')

        print(banner)
        prefix_operadora = input('Qual o prefixo da operadora? (2 dígitos)\n')
        prefix_om = input('Qual o prefixo da OM? (4 dígitos)\n')
        ddd_om = input('Qual é o DDD? (2 Dígitos)\n')
        trunk = None
        os.system('clear')

        print(banner)
        if trunk_pstn == '1':
           ip_gwe1 = input('Qual o IP do Gateway E1? ')
           tipo_tronco = 'E1'
           ip_tronco = ip_gwe1
        elif trunk_pstn == '2':
           ip_pstn = input('Qual o IP da Operadora? ')
           tipo_tronco = 'SIP Trunk'
           ip_tronco = ip_pstn
        else:
           print('A opção escolhida é inválida')
        os.system('clear')

        print(banner)
        prosseguir_2 = input(f'''
              Confirme as informações a baixo:
              \u2022 Hostname: {hostname}
              \u2022 NTP: {ip_ntp}
              \u2022 DNS: {ip_dns}
              \u2022 Senha de registro: {pass_reg}
              \u2022 Entroncamento: {tipo_tronco}
              \u2022 IP do entroncamento: {ip_tronco}

              Deseja prosseguir? ([s]im, [n]ão, [v]oltar)
              ''')
        if prosseguir_2 == 's':
            # --> Variáveis simples
            hostname_mach = socket.gethostname()
            loop = 's'
            include_gwe1 = '#include <pjsip.gwe1>'
            include_pstn = '#include <pjsip.pstn>'


            #============== Processamento ==================================
            os.system('clear')
            print(banner)
            # Checando a existencia dos arquivos

            check_pjsip = os.path.isfile('/etc/asterisk/pjsip.conf')
            check_extensions = os.path.isfile('/etc/asterisk/extensions.conf')
            check_features = os.path.isfile('/etc/asterisk/features.conf')

            if check_pjsip:
                print('pjsip.conf............... \u2714')
                shell('mv /etc/asterisk/pjsip.conf /etc/asterisk/pjsip.sample')

            else:
                print('pjsip.conf............... \u2718')

            if check_extensions:
                shell('mv /etc/asterisk/extensions.conf /etc/asterisk/extensions.sample')
                print('extensions.conf.......... \u2714')
            else:
                print('extensions.conf.......... \u2718')

            if check_features:
                shell('mv /etc/asterisk/features.conf /etc/asterisk/features.sample')
                print('features.conf............ \u2714')
            else:
                print('features.conf............ \u2718')

            # ---> extensions.ramais
            print('*----Criando extensions.ramais ----*\n')
            try:
                shell('touch /etc/asterisk/extensions.ramais')
                print('*----extensions.conf criado!----*\n')
                check_conf = '1'
            except:
                print('*----Erro ao criar o extensions.ramais----*\n')

            # ---> pjsip.ramais
            print('*----Criando pjsip.ramais ----*\n')
            try:
                shell('touch /etc/asterisk/pjsip.ramais')
                writing('/etc/asterisk/pjsip.ramais', pjsip_ramais)
                replace_pat('/etc/asterisk/pjsip.ramais', '%PASS%', pass_reg)
                print('*----pjsip.ramais criado!----*\n')
            except:
                print('*----pjsip.ramais não foi criado----*\n')


            while loop == 's':
                first_range = input('Digite o primeiro ramal do range: ')
                last_range = input('Digite o último ramal do range: ')
                header_pjsip = f'''; =========== DDR {str(first_range)} - {str(last_range)} =============
            '''
                writing_n('/etc/asterisk/pjsip.ramais', header_pjsip)
            # ----> Configuração do extensions.ramais   
                padrao_ramal = digit_process(int(first_range), int(last_range))
                writing_n('/etc/asterisk/extensions.ramais', extensions_ramais)
                replace_pat('/etc/asterisk/extensions.ramais', '%PADRAO_RAMAIS%', padrao_ramal )
                print('\n*----extensions.conf configurado----*\n')

                print('\n*----Configurando o pjsip.ramais----*\n')
                for ramal in range(int(first_range),int(last_range) + 1):
            # ----> Configurando pjsip.ramais       
                    writing_n('/etc/asterisk/pjsip.ramais', create_ramais)
                    replace_pat('/etc/asterisk/pjsip.ramais', '%NUM%', str(ramal))
                loop = input('Deseja configurar mais um range de ramais? (s ou n)\n')
                if loop == 's':
                    continue
                else:
                    break
            print('*----extensions.ramais e pjsip.ramais configurados----*')

            if config_ntp_dns == '1' or config_ntp_dns == '3':
                replace_line('/etc/systemd/timesyncd.conf', 'NTP=', f'NTP={ip_ntp}')
                shell('timedatectl set-timezone America/Sao_Paulo')
                print('\n*---- NTP alterado com sucesso ----*')

            if config_ntp_dns == '2' or config_ntp_dns == '3':
                replace_line('/etc/resolv.conf', 'nameserver', f'nameserver {ip_dns}')
                print('\n*---- DNS alterado com sucesso ----*')

            replace_pat('/etc/hostname', hostname_mach, hostname)
            replace_pat('/etc/hosts', hostname_mach, hostname)
            print('\n*---- Hostname alterado com sucesso ----*\n')


            try:
                print('*---- Criando pjsip.conf ----*\n')
                shell('touch /etc/asterisk/pjsip.conf')
                writing('/etc/asterisk/pjsip.conf', pjsip_padrao)
                print('*---- pjsip.conf criado! ----*\n')
            except:
                print('*---- Erro ao criar o pjsip.conf ----*\n')

            if trunk_pstn == '1' :
               print('*---- Configurando tronco E1 ----*\n')
               writing('/etc/asterisk/pjsip.conf', include_gwe1)
               shell('touch /etc/asterisk/pjsip.gwe1')
               writing('/etc/asterisk/pjsip.gwe1', pjsip_gwe1)
               replace_pat('/etc/asterisk/pjsip.gwe1', '%IP_GATE%', ip_gwe1)
               trunk = 'gwe1'


            elif trunk_pstn == '2' :
               print('*---- Configurando sip trunk com operadora ----*\n')
               writing('/etc/asterisk/pjsip.conf', include_pstn)
               shell('touch /etc/asterisk/pjsip.pstn')
               writing('/etc/asterisk/pjsip.pstn', pjsip_pstn)
               replace_pat('/etc/asterisk/pjsip.pstn', '%IP_OPERADORA%', ip_pstn)
               trunk = 'pstn'

            # ---> pjsip.transito
            print('*---- Criando pjsip.transito ----*\n')
            shell('touch /etc/asterisk/pjsip.transito')
            writing('/etc/asterisk/pjsip.transito', pjsip_transito)
            print('*---- pjsip.transito criado! ----*\n')


            # ---> extensions.conf
            print('\n*---- Criando extensions.conf ----*\n')
            shell('touch /etc/asterisk/extensions.conf')
            writing('/etc/asterisk/extensions.conf', extensions_conf)
            print('*---- extensions.conf criado! ----*\n')

            # ---> extensions.padrao
            shell('touch /etc/asterisk/extensions.padrao')
            writing('/etc/asterisk/extensions.padrao', extensions_padrao)
            replace_pat('/etc/asterisk/extensions.padrao', '%PREFIX_OM%', prefix_om)
            replace_pat('/etc/asterisk/extensions.padrao', '%DDD_OM%', ddd_om)
            replace_pat('/etc/asterisk/extensions.padrao', '%TRUNK%', trunk)
            replace_pat('/etc/asterisk/extensions.padrao', '%PREFIX_OPERADORA%', prefix_operadora)

            # ---> features.conf
            shell('touch /etc/asterisk/features.conf')
            writing('/etc/asterisk/features.conf', features_conf)

            # ---> Verificando configurações de rede



            #------> Listando o que foi criado
            print('''
                  ******************************************************************
                  ******************************************************************
                  ******************************************************************\n''')
            check_create_conf = ''
            if os.path.isfile('/etc/asterisk/extensions.conf'):
                check_create_conf += '\nextensions.conf ............ OK'
            else:
                check_create_conf += '\nextensions.conf ............ Não Criado'
            if os.path.isfile('/etc/asterisk/pjsip.conf'):
                check_create_conf += '\npjsip.conf ............ OK'
            else:
                check_create_conf += '\npjsip.conf ............ Não Criado'
            if os.path.isfile('/etc/asterisk/features.conf'):
                check_create_conf += '\nfeatures.conf ............ OK'
            else:
                check_create_conf += '\nfeatures.conf ............ Não Criado'
            if os.path.isfile('/etc/asterisk/pjsip.ramais'):
                check_create_conf += '\npjsip.ramais ............ OK'
            else:
                check_create_conf += '\npjsip.ramais ............ Não Criado'
            if os.path.isfile('/etc/asterisk/extensions.ramais'):
                check_create_conf += '\nextensions.ramais ............ OK'
            else:
                check_create_conf += '\nextensions.ramais ............ Não Criado'
            if os.path.isfile('/etc/asterisk/extensions.padrao'):
                check_create_conf += '\nextensions.padrao ............ OK'
            else:
                check_create_conf += '\nextensions.padrao ............ Não Criado'
            if os.path.isfile('/etc/asterisk/pjsip.transito'):
                check_create_conf += '\npjsip.transito ............ OK'
            else:
                check_create_conf += '\npjsip.transito ............ Não Criado'
            if os.path.isfile('/etc/asterisk/pjsip.gwe1'):
                check_create_conf += '\npjsip.gwe1 ............ OK'
            else:
                check_create_conf += '\npjsip.gwe1 ............ Não Criado'
            if os.path.isfile('/etc/asterisk/pjsip.pstn'):
                check_create_conf += '\npjsip.pstn ............ OK'
            else:
                check_create_conf += '\npjsip.pstn ............ Não Criado'

            print(check_create_conf)
        elif prosseguir_2 == 'n':
            print('Programa finalizado!')
        elif prosseguir_2 == 'v':
            continue
        
        opcao_menu = input('Deseja fazer mais alguma configuração? (s/n)\n')
        if opcao_menu == 's':
            continue
        elif opcao_menu == 'n':
            break

    elif entrada_inicial == '3':

    # Versão 1.3.3 (03-07-2024)
    # Definiçoes
        def replace_pat(filename, pattern, replacement):
           with open(filename, 'r') as file:
               text = file.read()


           text = re.sub(pattern, replacement, text)


           with open(filename, 'w') as file:
               file.write(text)

        def shell(command):
           subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        def correcao_mac(mac):
           letras_num = 'abcdefghijklmnopqrstuvwxyz0123456789'
           var = mac.lower()
           palavra = ''


           for letra in var:
               if letra in letras_num:
                   palavra += letra
           return palavra

        def write_text(path, text):
            with open(path, 'w') as f:
                f.write(text)

        # Declaração de variáveis
        quant_arquivos = 0
        lista_modelos = ['cp-3905', 'cp-7821', 'cp-7942', 'cp-8845', 'cp-8865', 'cp-9845', \
                         'gxp-1615', 'gxp-1625', 'gxp-2170', 'yealink-22p']

        # Configuração dos telefones
        cp_3905 = '''<device>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<devicePool>
    <dateTimeSetting>
        <dateTemplate>D/M/Y</dateTemplate>
        <timeZone>SA Eastern Standard Time</timeZone>
        <ntps>
        <ntp>
            <!-- SERVIDOR DE DATA e HORA - não altere  -->
            <name>%NTP%</name>
            <ntpMode>Unicast</ntpMode>
        </ntp>
        </ntps>
    </dateTimeSetting>
    <callManagerGroup>
        <members>
        <member priority="0">
            <callManager>
                <ports>
                    <ethernetPhonePort>2000</ethernetPhonePort>
                    <sipPort>5060</sipPort>
                    <securedSipPort>5061</securedSipPort>
                </ports>

                <!-- IP ou FQDN (host) do SERVIDOR REGISTRO SIP (seu Asterisk, por exemplo) -->
                <processNodeName>$asterisk</processNodeName>

            </callManager>
        </member>
        </members>
    </callManagerGroup>
</devicePool>
<sipProfile>
    <sipProxies>
        <backupProxy></backupProxy>
        <backupProxyPort>5060</backupProxyPort>
        <emergencyProxy></emergencyProxy>
        <emergencyProxyPort></emergencyProxyPort>
        <outboundProxy></outboundProxy>
        <outboundProxyPort></outboundProxyPort>
        <registerWithProxy>true</registerWithProxy>
    </sipProxies>
    <sipCallFeatures>
        <cnfJoinEnabled>true</cnfJoinEnabled>
        <callForwardURI>x-serviceuri-cfwdall</callForwardURI>
        <callPickupURI>x-cisco-serviceuri-pickup</callPickupURI>
        <callPickupListURI>x-cisco-serviceuri-opickup</callPickupListURI>

<callPickupGroupURI>x-cisco-serviceuri-gpickup</callPickupGroupURI>
        <meetMeServiceURI>x-cisco-serviceuri-meetme</meetMeServiceURI>

<abbreviatedDialURI>x-cisco-serviceuri-abbrdial</abbreviatedDialURI>
        <rfc2543Hold>false</rfc2543Hold>
        <callHoldRingback>2</callHoldRingback>
        <localCfwdEnable>true</localCfwdEnable>
        <semiAttendedTransfer>true</semiAttendedTransfer>
        <anonymousCallBlock>2</anonymousCallBlock>
        <callerIdBlocking>2</callerIdBlocking>
        <dndControl>0</dndControl>
        <remoteCcEnable>true</remoteCcEnable>
    </sipCallFeatures>
    <sipStack>
        <sipInviteRetx>6</sipInviteRetx>
        <sipRetx>10</sipRetx>
        <timerInviteExpires>180</timerInviteExpires>
        <timerRegisterExpires>3600</timerRegisterExpires>
        <timerRegisterDelta>5</timerRegisterDelta>
        <timerKeepAliveExpires>3600</timerKeepAliveExpires>
        <timerSubscribeExpires>3600</timerSubscribeExpires>
        <timerSubscribeDelta>5</timerSubscribeDelta>
        <timerT1>500</timerT1>
        <timerT2>4000</timerT2>
        <maxRedirects>70</maxRedirects>
        <remotePartyID>false</remotePartyID>
        <userInfo>None</userInfo>
    </sipStack>
    <autoAnswerTimer>1</autoAnswerTimer>
    <autoAnswerAltBehavior>false</autoAnswerAltBehavior>
    <autoAnswerOverride>true</autoAnswerOverride>
    <transferOnhookEnabled>false</transferOnhookEnabled>
    <enableVad>false</enableVad>
    <dtmfAvtPayload>101</dtmfAvtPayload>
    <dtmfDbLevel>3</dtmfDbLevel>
    <dtmfOutofBand>avt</dtmfOutofBand>
    <alwaysUsePrimeLine>false</alwaysUsePrimeLine>
    <alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
    <kpml>3</kpml>

    <!-- Seu nome com até 13 caracteres, sem espaços -->
    <phoneLabel>$nome</phoneLabel>

    <stutterMsgWaiting>1</stutterMsgWaiting>
    <callStats>false</callStats>

<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
    <disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
    <sipLines>
        <line button="1">
        <featureID>9</featureID>

        <!-- IP ou FQDN (host) do SERVIDOR REGISTRO SIP (seu Asterisk, por exemplo) -->
        <proxy>%ASTER%</proxy>
        <port>5060</port>

        <!-- Usuário SIP ou ramal -->
        <featureLabel>%RAMAL%</featureLabel>

        <!-- Usuário SIP ou ramal -->
        <name>%RAMAL%</name>

        <!-- Usuário SIP ou ramal -->
        <displayName>%NOME%</displayName>

        <!-- Usuário SIP ou ramal -->
        <authName>%RAMAL%</authName>

        <!-- Usuário SIP ou ramal -->
        <contact>%RAMAL%</contact>

        <!-- SENHA da conta SIP -->
        <authPassword>%PASS%</authPassword>

        <autoAnswer>
            <autoAnswerEnabled>2</autoAnswerEnabled>
        </autoAnswer>
        <callWaiting>3</callWaiting>
        <sharedLine>false</sharedLine>
        <messageWaitingLampPolicy>1</messageWaitingLampPolicy>
        <messagesNumber>*97</messagesNumber>
        <ringSettingIdle>4</ringSettingIdle>
        <ringSettingActive>5</ringSettingActive>

        <forwardCallInfoDisplay>
            <callerName>true</callerName>
            <callerNumber>false</callerNumber>
            <redirectedNumber>false</redirectedNumber>
            <dialedNumber>true</dialedNumber>
        </forwardCallInfoDisplay>
        </line>
    </sipLines>

    <!-- Parâmetros da conta SIP -->
    <voipControlPort>5060</voipControlPort>
    <startMediaPort>10000</startMediaPort>
    <stopMediaPort>20000</stopMediaPort>

    <dscpForAudio>184</dscpForAudio>
    <ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
    <dialTemplate>dialplan.xml</dialTemplate>
    <softKeyFile></softKeyFile>
</sipProfile>
<commonProfile>
    <phonePassword></phonePassword>
    <backgroundImageAccess>true</backgroundImageAccess>
    <callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>

<!-- Versao do Firmware para auto upgrade (se estiver na mesma pasta TFTP) -->
<loadInformation>CP3905.9-4-1SR2-2</loadInformation>

<vendorConfig>
    <disableSpeaker>false</disableSpeaker>
    <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
    <pcPort>0</pcPort>
    <settingsAccess>1</settingsAccess>
    <garp>0</garp>
    <voiceVlanAccess>0</voiceVlanAccess>
    <videoCapability>0</videoCapability>
    <autoSelectLineEnable>0</autoSelectLineEnable>
    <webAccess>1</webAccess>
    <daysDisplayNotActive>1,2,3,4,5,6,7</daysDisplayNotActive>
    <displayOnTime>00:00</displayOnTime>
    <displayOnDuration>00:00</displayOnDuration>
    <displayIdleTimeout>00:00</displayIdleTimeout>
    <spanToPCPort>1</spanToPCPort>
    <loggingDisplay>1</loggingDisplay>
    <loadServer></loadServer>
</vendorConfig>
<userLocale>
    <name></name>
    <uid></uid>
    <langCode>Brazil</langCode>
    <version>1.0.0.0-1</version>
    <winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
    <name>Brazil</name>
    <uid></uid>
    <version>1.0.0.0-1</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<servicesURL></servicesURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<capfAuthMode>0</capfAuthMode>
<capfList>
    <capf>
        <phonePort>3804</phonePort>
    </capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
</device>



        '''
        cp_7821 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
    <sshUserId>cisco</sshUserId>
    <sshPassword>cisco</sshPassword>
    <sshAccess>0</sshAccess>
    <sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>j9-tzdata.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
        <ntps>
            <ntp>
                <name>%NTP%</name>
            <ntpMode>Unicast</ntpMode>
            </ntp>
        </ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<address></address>
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>false</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
            <authName>%RAMAL%</authName> 
            <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber>%RAMAL%</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact>%RAMAL%</contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
            <authName></authName>
            <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>



</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>sip78xx.12-5-1SR1-4</loadInformation>
<vendorConfig>
    <defaultWallpaperFile></defaultWallpaperFile>
    <disableSpeaker>false</disableSpeaker>
    <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
    <enableMuteFeature>false</enableMuteFeature>
    <enableGroupListen>true</enableGroupListen>
    <holdResumeKey>1</holdResumeKey>
    <recentsSoftKey>1</recentsSoftKey>
    <dfBit>1</dfBit>
    <pcPort>0</pcPort>
    <spanToPCPort>1</spanToPCPort>
    <garp>0</garp>
    <rtcp>1</rtcp>
    <videoRtcp>1</videoRtcp>
    <voiceVlanAccess>0</voiceVlanAccess>
    <videoCapability>1</videoCapability>
    <hideVideoByDefault>0</hideVideoByDefault>
    <separateMute>0</separateMute>
    <ciscoCamera>1</ciscoCamera>
    <usb1>1</usb1>
    <usb2>1</usb2>
    <usbClasses>0,1,2</usbClasses>
    <sdio>1</sdio>
    <wifi>1</wifi>
    <bluetooth>1</bluetooth>
    <bluetoothProfile>0,1</bluetoothProfile>
    <btpbap>0</btpbap>
    <bthfu>0</bthfu>
    <ehookEnable>0</ehookEnable>
    <autoSelectLineEnable>1</autoSelectLineEnable>
    <autoCallSelect>1</autoCallSelect>
    <incomingCallToastTimer>10</incomingCallToastTimer>
    <dialToneFromReleaseKey>0</dialToneFromReleaseKey>
    <joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
    <minimumRingVolume></minimumRingVolume>
    <simplifiedNewCall>0</simplifiedNewCall>
    <actionableAlert>0</actionableAlert>
    <showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
    <kemOneColumn>0</kemOneColumn>
    <lineMode>0</lineMode>
    <allCallsOnPrimary>0</allCallsOnPrimary>
    <softKeyControl>0</softKeyControl>
    <settingsAccess>1</settingsAccess>
    <webProtocol>0</webProtocol>
    <webAccess>0</webAccess>
    <webAdmin>1</webAdmin>
    <adminPassword></adminPassword>
    <sshAccess>0</sshAccess>
    <detectCMConnectionFailure>0</detectCMConnectionFailure>
    <g722CodecSupport>1</g722CodecSupport>
    <handsetWidebandEnable>2</handsetWidebandEnable>
    <headsetWidebandEnable>2</headsetWidebandEnable>
    <headsetWidebandUIControl>1</headsetWidebandUIControl>
    <handsetWidebandUIControl>1</handsetWidebandUIControl>
    <daysDisplayNotActive>1,7</daysDisplayNotActive>
    <displayOnTime>08:00</displayOnTime>
    <displayOnDuration>10:00</displayOnDuration>
    <displayIdleTimeout>00:10</displayIdleTimeout>
    <displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
    <displayRefreshRate>0</displayRefreshRate>
    <daysBacklightNotActive>1,7</daysBacklightNotActive>
    <backlightOnTime>08:00</backlightOnTime>
    <backlightOnDuration>10:00</backlightOnDuration>
    <backlightIdleTimeout>00:10</backlightIdleTimeout>
    <backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
    <recordingTone>0</recordingTone>
    <recordingToneLocalVolume>100</recordingToneLocalVolume>
    <recordingToneRemoteVolume>50</recordingToneRemoteVolume>
    <recordingToneDuration></recordingToneDuration>
    <moreKeyReversionTimer>5</moreKeyReversionTimer>
    <peerFirmwareSharing>0</peerFirmwareSharing>
    <loadServer></loadServer>
    <problemReportUploadURL></problemReportUploadURL>
    <enableCdpSwPort>1</enableCdpSwPort>
    <enableCdpPcPort>0</enableCdpPcPort>
    <enableLldpSwPort>1</enableLldpSwPort>
    <enableLldpPcPort>0</enableLldpPcPort>
    <cdpEnable>true</cdpEnable>
    <outOfRangeAlert>0</outOfRangeAlert>
    <scanningMode>2</scanningMode>
    <applicationURL></applicationURL>
    <appButtonTimer>0</appButtonTimer>
    <appButtonPriority>0</appButtonPriority>
    <specialNumbers></specialNumbers>
    <sendKeyAction>0</sendKeyAction>
    <powerOffWhenCharging>0</powerOffWhenCharging>
    <homeScreen>0</homeScreen>
    <accessContacts>1</accessContacts>
    <accessFavorites>1</accessFavorites>
    <accessVoicemail>1</accessVoicemail>
    <accessApps>1</accessApps>
    </vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL>http://10.52.66.23:5000/contactsMenu?company=FAB_RCAER&amp;group=CCA_RJ</directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName>%ASTER%</processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
        '''
        cp_7942 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
    <sshUserId>cisco</sshUserId>
    <sshPassword>cisco</sshPassword>
    <sshAccess>0</sshAccess>
    <sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>tzupdaterTropico.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
        <ntps>
            <ntp>
                <name>%NTP%</name>
            <ntpMode>Unicast</ntpMode>
            </ntp>
        </ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<!--address>VSS.tropiconet.com</address-->
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>true</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
            <authName>%RAMAL%</authName> 
            <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
            <authName></authName>
            <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>4</busyTrigger>
</line>



</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>SIP42.9-4-2SR3-1S</loadInformation>
<vendorConfig>
    <defaultWallpaperFile></defaultWallpaperFile>
    <disableSpeaker>false</disableSpeaker>
    <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
    <enableMuteFeature>false</enableMuteFeature>
    <enableGroupListen>true</enableGroupListen>
    <holdResumeKey>1</holdResumeKey>
    <recentsSoftKey>1</recentsSoftKey>
    <dfBit>1</dfBit>
    <pcPort>0</pcPort>
    <spanToPCPort>1</spanToPCPort>
    <garp>0</garp>
    <rtcp>1</rtcp>
    <videoRtcp>1</videoRtcp>
    <voiceVlanAccess>0</voiceVlanAccess>
    <videoCapability>1</videoCapability>
    <hideVideoByDefault>0</hideVideoByDefault>
    <separateMute>0</separateMute>
    <ciscoCamera>1</ciscoCamera>
    <usb1>1</usb1>
    <usb2>1</usb2>
    <usbClasses>0,1,2</usbClasses>
    <sdio>1</sdio>
    <wifi>1</wifi>
    <bluetooth>1</bluetooth>
    <bluetoothProfile>0,1</bluetoothProfile>
    <btpbap>0</btpbap>
    <bthfu>0</bthfu>
    <ehookEnable>0</ehookEnable>
    <autoSelectLineEnable>1</autoSelectLineEnable>
    <autoCallSelect>1</autoCallSelect>
    <incomingCallToastTimer>10</incomingCallToastTimer>
    <dialToneFromReleaseKey>0</dialToneFromReleaseKey>
    <joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
    <minimumRingVolume></minimumRingVolume>
    <simplifiedNewCall>0</simplifiedNewCall>
    <actionableAlert>0</actionableAlert>
    <showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
    <kemOneColumn>0</kemOneColumn>
    <lineMode>0</lineMode>
    <allCallsOnPrimary>0</allCallsOnPrimary>
    <softKeyControl>0</softKeyControl>
    <settingsAccess>1</settingsAccess>
    <webProtocol>0</webProtocol>
    <webAccess>0</webAccess>
    <webAdmin>1</webAdmin>
    <adminPassword></adminPassword>
    <sshAccess>0</sshAccess>
    <detectCMConnectionFailure>0</detectCMConnectionFailure>
    <g722CodecSupport>1</g722CodecSupport>
    <handsetWidebandEnable>2</handsetWidebandEnable>
    <headsetWidebandEnable>2</headsetWidebandEnable>
    <headsetWidebandUIControl>1</headsetWidebandUIControl>
    <handsetWidebandUIControl>1</handsetWidebandUIControl>
    <daysDisplayNotActive>1,7</daysDisplayNotActive>
    <displayOnTime>08:00</displayOnTime>
    <displayOnDuration>10:00</displayOnDuration>
    <displayIdleTimeout>00:10</displayIdleTimeout>
    <displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
    <displayRefreshRate>0</displayRefreshRate>
    <daysBacklightNotActive>1,7</daysBacklightNotActive>
    <backlightOnTime>08:00</backlightOnTime>
    <backlightOnDuration>10:00</backlightOnDuration>
    <backlightIdleTimeout>00:10</backlightIdleTimeout>
    <backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
    <recordingTone>0</recordingTone>
    <recordingToneLocalVolume>100</recordingToneLocalVolume>
    <recordingToneRemoteVolume>50</recordingToneRemoteVolume>
    <recordingToneDuration></recordingToneDuration>
    <moreKeyReversionTimer>5</moreKeyReversionTimer>
    <peerFirmwareSharing>0</peerFirmwareSharing>
    <loadServer></loadServer>
    <problemReportUploadURL></problemReportUploadURL>
    <enableCdpSwPort>1</enableCdpSwPort>
    <enableCdpPcPort>0</enableCdpPcPort>
    <enableLldpSwPort>1</enableLldpSwPort>
    <enableLldpPcPort>0</enableLldpPcPort>
    <cdpEnable>true</cdpEnable>
    <outOfRangeAlert>0</outOfRangeAlert>
    <scanningMode>2</scanningMode>
    <applicationURL></applicationURL>
    <appButtonTimer>0</appButtonTimer>
    <appButtonPriority>0</appButtonPriority>
    <specialNumbers></specialNumbers>
    <sendKeyAction>0</sendKeyAction>
    <powerOffWhenCharging>0</powerOffWhenCharging>
    <homeScreen>0</homeScreen>
    <accessContacts>1</accessContacts>
    <accessFavorites>1</accessFavorites>
    <accessVoicemail>1</accessVoicemail>
    <accessApps>1</accessApps>
    </vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>1</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName></processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="1" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="1" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="1" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
        '''
        cp_8845 = '''<?xml version="1.0" encoding="UTF-8"?>
    <device>
    <fullConfig>true</fullConfig>
    <deviceProtocol>SIP</deviceProtocol>
        <sshUserId>cisco</sshUserId>
        <sshPassword>cisco</sshPassword>
        <sshAccess>0</sshAccess>
        <sshPort>22</sshPort>
    <ipAddressMode>0</ipAddressMode>
    <allowAutoConfig>true</allowAutoConfig>
    <ipPreferenceModeControl>0</ipPreferenceModeControl>
    <tzdata>
    <tzolsonversion>tzdata2019c</tzolsonversion>
    <tzupdater>j9-tzdata.jar</tzupdater>
    </tzdata>
    <devicePool>
    <revertPriority>0</revertPriority>
    <name>Default</name>
    <dateTimeSetting>
    <name>CMLocal</name>
    <dateTemplate>D/M/Y</dateTemplate>
    <timeZone>SA Eastern Standard Time</timeZone>
            <ntps>
                <ntp>
                    <name>%NTP%</name>
                <ntpMode>Unicast</ntpMode>
                </ntp>
            </ntps>
    </dateTimeSetting>
    <callManagerGroup>
    <name>Default</name>
    <tftpDefault>true</tftpDefault>
    <members>
    <member priority="0">
    <callManager>
    <name>ASTERISK</name>
    <description>PBXSIP</description>
    <ports>
    <ethernetPhonePort>2000</ethernetPhonePort>
    <sipPort>5060</sipPort>
    <securedSipPort>5061</securedSipPort>
    <mgcpPorts>
    <listen>2427</listen>
    <keepAlive>2428</keepAlive>
    </mgcpPorts>
    </ports>
    <processNodeName>%ASTER%</processNodeName>
    </callManager>
    </member>
    </members>
    </callManagerGroup>
    <srstInfo uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
    <name>Disable</name>
    <srstOption>Disable</srstOption>
    <userModifiable>false</userModifiable>
    <ipAddr1/>
    <port1>2000</port1>
    <ipAddr2/>
    <port2>2000</port2>
    <ipAddr3/>
    <port3>2000</port3>
    <sipIpAddr1/>
    <sipPort1>5060</sipPort1>
    <sipIpAddr2/>
    <sipPort2>5060</sipPort2>
    <sipIpAddr3/>
    <sipPort3>5060</sipPort3>
    <isSecure>false</isSecure>
    </srstInfo>
    <mlppDomainId>-1</mlppDomainId>
    <mlppIndicationStatus>Default</mlppIndicationStatus>
    <preemption>Default</preemption>
    <connectionMonitorDuration>120</connectionMonitorDuration>
    </devicePool>
    <TVS>
    <members>
    <member priority="0">
    <port>2445</port>
    <!--servidor para validar arquivos de configuração criptografados-->
    <address></address>
    </member>
    </members>
    </TVS>
    <sipProfile>
    <sipProxies>
    <backupProxy>USECALLMANAGER</backupProxy>
    <backupProxyPort>5060</backupProxyPort>
    <emergencyProxy>USECALLMANAGER</emergencyProxy>
    <emergencyProxyPort>5060</emergencyProxyPort>
    <outboundProxy>USECALLMANAGER</outboundProxy>
    <outboundProxyPort>5060</outboundProxyPort>
    <registerWithProxy>true</registerWithProxy>
    </sipProxies>
    <sipCallFeatures>
    <cnfJoinEnabled>true</cnfJoinEnabled>
    <callForwardURI>7</callForwardURI>
    <callPickupURI>x-cisco-serviceuri-pickup</callPickupURI>
    <callPickupListURI/>
    <callPickupGroupURI>x-cisco-serviceuri-gpickup</callPickupGroupURI>
    <meetMeServiceURI/>
    <abbreviatedDialURI/>
    <rfc2543Hold>false</rfc2543Hold>
    <callHoldRingback>1</callHoldRingback>
    <localCfwdEnable>true</localCfwdEnable>
    <semiAttendedTransfer>true</semiAttendedTransfer>
    <anonymousCallBlock>2</anonymousCallBlock>
    <callerIdBlocking>0</callerIdBlocking>
    <remoteCcEnable>true</remoteCcEnable>
    <retainForwardInformation>false</retainForwardInformation>
    </sipCallFeatures>
    <sipStack>
    <sipInviteRetx>6</sipInviteRetx>
    <sipRetx>10</sipRetx>
    <timerInviteExpires>180</timerInviteExpires>
    <timerRegisterExpires>3600</timerRegisterExpires>
    <timerRegisterDelta>5</timerRegisterDelta>
    <timerKeepAliveExpires>3600</timerKeepAliveExpires>
    <timerSubscribeExpires>3600</timerSubscribeExpires>
    <timerSubscribeDelta>5</timerSubscribeDelta>
    <timerT1>500</timerT1>
    <timerT2>4000</timerT2>
    <maxRedirects>70</maxRedirects>
    <remotePartyID>true</remotePartyID>
    <userInfo>None</userInfo>
    </sipStack>
    <autoAnswerTimer>1</autoAnswerTimer>
    <autoAnswerAltBehavior>false</autoAnswerAltBehavior>
    <autoAnswerOverride>true</autoAnswerOverride>
    <transferOnhookEnabled>false</transferOnhookEnabled>
    <enableVad>false</enableVad>
    <preferredCodec>g711alaw</preferredCodec>
    <dtmfAvtPayload>101</dtmfAvtPayload>
    <dtmfDbLevel>3</dtmfDbLevel>
    <dtmfOutofBand>avt</dtmfOutofBand>
    <kpml>3</kpml>
    <phoneLabel>%RAMAL%</phoneLabel>
    <stutterMsgWaiting>2</stutterMsgWaiting>
    <callStats>true</callStats>
    <offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
    <T302Timer>15000</T302Timer>
    <silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
    <disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
    <poundEndOfDial>false</poundEndOfDial>
    <startMediaPort>16384</startMediaPort>
    <stopMediaPort>32766</stopMediaPort>
    <sipLines>
    <line button="1" lineIndex="1">
    <featureID>9</featureID>
    <featureLabel/>
    <proxy>USECALLMANAGER</proxy>
    <port>5060</port>
    <name>%RAMAL%</name>
                <authName>%RAMAL%</authName> 
                <authPassword>%PASS</authPassword>
    <displayName>%NOME%</displayName>
    <autoAnswer>
    <autoAnswerEnabled>2</autoAnswerEnabled>
    </autoAnswer>
    <callWaiting>3</callWaiting>
    <sharedLine>false</sharedLine>
    <messageWaitingLampPolicy>1</messageWaitingLampPolicy>
    <messageWaitingAMWI>1</messageWaitingAMWI>
    <messagesNumber></messagesNumber>
    <ringSettingIdle>4</ringSettingIdle>
    <ringSettingActive>5</ringSettingActive>
    <contact></contact>
    <forwardCallInfoDisplay>
    <callerName>true</callerName>
    <callerNumber>true</callerNumber>
    <redirectedNumber>true</redirectedNumber>
    <dialedNumber>true</dialedNumber>
    </forwardCallInfoDisplay>
    <maxNumCalls>4</maxNumCalls>
    <busyTrigger>1</busyTrigger>
    </line>

    <!--

    <line button="2" lineIndex="2">
    <featureID>9</featureID>
    <featureLabel/>
    <proxy>USECALLMANAGER</proxy>
    <port>5060</port>
    <name></name>
                <authName></authName>
                <authPassword></authPassword>
    <displayName></displayName>
    <autoAnswer>
    <autoAnswerEnabled>2</autoAnswerEnabled>
    </autoAnswer>
    <callWaiting>3</callWaiting>
    <sharedLine>false</sharedLine>
    <messageWaitingLampPolicy>1</messageWaitingLampPolicy>
    <messageWaitingAMWI>1</messageWaitingAMWI>
    <messagesNumber></messagesNumber>
    <ringSettingIdle>4</ringSettingIdle>
    <ringSettingActive>5</ringSettingActive>
    <contact></contact>
    <forwardCallInfoDisplay>
    <callerName>true</callerName>
    <callerNumber>true</callerNumber>
    <redirectedNumber>true</redirectedNumber>
    <dialedNumber>true</dialedNumber>
    </forwardCallInfoDisplay>
    <maxNumCalls>4</maxNumCalls>
    <busyTrigger>1</busyTrigger>
    </line>

    -->

    <!--

    <line button="3" lineIndex="3">
    <featureID>9</featureID>
    <featureLabel/>
    <proxy>USECALLMANAGER</proxy>
    <port>5060</port>
    <name></name>
                <authName></authName>
                <authPassword></authPassword>
    <displayName></displayName>
    <autoAnswer>
    <autoAnswerEnabled>2</autoAnswerEnabled>
    </autoAnswer>
    <callWaiting>3</callWaiting>
    <sharedLine>false</sharedLine>
    <messageWaitingLampPolicy>1</messageWaitingLampPolicy>
    <messageWaitingAMWI>1</messageWaitingAMWI>
    <messagesNumber></messagesNumber>
    <ringSettingIdle>4</ringSettingIdle>
    <ringSettingActive>5</ringSettingActive>
    <contact></contact>
    <forwardCallInfoDisplay>
    <callerName>true</callerName>
    <callerNumber>true</callerNumber>
    <redirectedNumber>true</redirectedNumber>
    <dialedNumber>true</dialedNumber>
    </forwardCallInfoDisplay>
    <maxNumCalls>4</maxNumCalls>
    <busyTrigger>1</busyTrigger>
    </line>

    -->


    </sipLines>
    <externalNumberMask/>
    <voipControlPort>5060</voipControlPort>
    <dscpForAudio>184</dscpForAudio>
    <dscpVideo>136</dscpVideo>
    <dscpForTelepresence>128</dscpForTelepresence>
    <ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
    <dialTemplate>dialplan.xml</dialTemplate>
    <softKeyFile>SofteyCISCO.xml</softKeyFile>
    <alwaysUsePrimeLine>false</alwaysUsePrimeLine>
    <alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
    </sipProfile>
    <MissedCallLoggingOption>10</MissedCallLoggingOption>
    <commonProfile>
    <phonePassword/>
    <backgroundImageAccess>true</backgroundImageAccess>
    <callLogBlfEnabled>2</callLogBlfEnabled>
    </commonProfile>
    <loadInformation>sip8845_65.12-5-1SR2-2</loadInformation>

    <vendorConfig>
        <defaultWallpaperFile/>
        <disableSpeaker>false</disableSpeaker>
        <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
        <enableMuteFeature>false</enableMuteFeature>
        <enableGroupListen>true</enableGroupListen>
        <holdResumeKey>1</holdResumeKey>
        <recentsSoftKey>1</recentsSoftKey>
        <dfBit>1</dfBit>
        <pcPort>0</pcPort>
        <spanToPCPort>1</spanToPCPort>
        <garp>0</garp>
        <rtcp>1</rtcp>
        <videoRtcp>1</videoRtcp>
        <voiceVlanAccess>0</voiceVlanAccess>
        <videoCapability>1</videoCapability>
        <hideVideoByDefault>0</hideVideoByDefault>
        <separateMute>0</separateMute>
        <ciscoCamera>1</ciscoCamera>
        <usb1>1</usb1>
        <usb2>1</usb2>
        <usbClasses>0,1,2</usbClasses>
        <sdio>1</sdio>
        <wifi>1</wifi>
        <bluetooth>1</bluetooth>
        <bluetoothProfile>0,1</bluetoothProfile>
        <btpbap>0</btpbap>
        <bthfu>0</bthfu>
        <ehookEnable>0</ehookEnable>
        <autoSelectLineEnable>1</autoSelectLineEnable>
        <autoCallSelect>1</autoCallSelect>
        <incomingCallToastTimer>10</incomingCallToastTimer>
        <dialToneFromReleaseKey>0</dialToneFromReleaseKey>
        <joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
        <minimumRingVolume/>
        <simplifiedNewCall>0</simplifiedNewCall>
        <actionableAlert>0</actionableAlert>
        <showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
        <kemOneColumn>0</kemOneColumn>
        <lineMode>0</lineMode>
        <allCallsOnPrimary>0</allCallsOnPrimary>
        <softKeyControl>0</softKeyControl>
        <settingsAccess>1</settingsAccess>
        <webProtocol>0</webProtocol>
        <webAccess>0</webAccess>
        <webAdmin>1</webAdmin>
        <adminPassword/>
        <sshAccess>0</sshAccess>
        <detectCMConnectionFailure>0</detectCMConnectionFailure>
        <g722CodecSupport>1</g722CodecSupport>
        <handsetWidebandEnable>2</handsetWidebandEnable>
        <headsetWidebandEnable>2</headsetWidebandEnable>
        <headsetWidebandUIControl>1</headsetWidebandUIControl>
        <handsetWidebandUIControl>1</handsetWidebandUIControl>
        <daysDisplayNotActive>1,7</daysDisplayNotActive>
        <displayOnTime>08:00</displayOnTime>
        <displayOnDuration>10:00</displayOnDuration>
        <displayIdleTimeout>00:10</displayIdleTimeout>
        <displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
        <displayRefreshRate>0</displayRefreshRate>
        <daysBacklightNotActive>1,7</daysBacklightNotActive>
        <backlightOnTime>08:00</backlightOnTime>
        <backlightOnDuration>10:00</backlightOnDuration>
        <backlightIdleTimeout>00:10</backlightIdleTimeout>
        <backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
        <recordingTone>0</recordingTone>
        <recordingToneLocalVolume>100</recordingToneLocalVolume>
        <recordingToneRemoteVolume>50</recordingToneRemoteVolume>
        <recordingToneDuration/>
        <moreKeyReversionTimer>5</moreKeyReversionTimer>
        <peerFirmwareSharing>0</peerFirmwareSharing>
        <loadServer/>
        <problemReportUploadURL/>
        <enableCdpSwPort>1</enableCdpSwPort>
        <enableCdpPcPort>0</enableCdpPcPort>
        <enableLldpSwPort>1</enableLldpSwPort>
        <enableLldpPcPort>0</enableLldpPcPort>
        <cdpEnable>true</cdpEnable>
        <outOfRangeAlert>0</outOfRangeAlert>
        <scanningMode>2</scanningMode>
        <applicationURL/>
        <appButtonTimer>0</appButtonTimer>
        <appButtonPriority>0</appButtonPriority>
        <specialNumbers/>
        <sendKeyAction>0</sendKeyAction>
        <powerOffWhenCharging>0</powerOffWhenCharging>
        <homeScreen>0</homeScreen>
        <accessContacts>1</accessContacts>
        <accessFavorites>1</accessFavorites>
        <accessVoicemail>1</accessVoicemail>
        <accessApps>1</accessApps>
        </vendorConfig>




    <commonConfig>
    </commonConfig>
    <enterpriseConfig>
    </enterpriseConfig>
    <versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
    <userLocale>
    <name></name>
    <uid>1</uid>
    <langCode>pt</langCode>
    <version>8.5.0.0(1)</version>
    <winCharSet>iso-8859-1</winCharSet>
    </userLocale>
    <networkLocale/>
    <networkLocaleInfo>
    <name>brazil</name>
    <uid>64</uid>
    <version>8.5.0.0(1)</version>
    </networkLocaleInfo>
    <deviceSecurityMode>1</deviceSecurityMode>
    <idleTimeout>0</idleTimeout>
    <authenticationURL/>
    <directoryURL></directoryURL>
    <idleURL/>
    <informationURL/>
    <messagesURL/>
    <proxyServerURL/>
    <servicesURL/>
    <secureAuthenticationURL/>
    <secureDirectoryURL/>
    <secureIdleURL/>
    <secureInformationURL/>
    <secureMessagesURL/>
    <secureServicesURL/>
    <dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
    <dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
    <dscpForCm2Dvce>96</dscpForCm2Dvce>
    <transportLayerProtocol>2</transportLayerProtocol>
    <phonePersonalization>0</phonePersonalization>
    <rollover>0</rollover>
    <singleButtonBarge>0</singleButtonBarge>
    <joinAcrossLines>0</joinAcrossLines>
    <autoCallPickupEnable>false</autoCallPickupEnable>
    <blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
    <blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
    <capfAuthMode>0</capfAuthMode>
    <capfList>
    <capf>
    <phonePort>3804</phonePort>
    <processNodeName>$asterisk</processNodeName>
    </capf>
    </capfList>
    <certHash/>
    <encrConfig>false</encrConfig>
    <advertiseG722Codec>1</advertiseG722Codec>
    <mobility>
    <handoffdn/>
    <dtmfdn/>
    <ivrdn/>
    <dtmfHoldCode>*81</dtmfHoldCode>
    <dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
    <dtmfResumeCode>*83</dtmfResumeCode>
    <dtmfTxfCode>*84</dtmfTxfCode>
    <dtmfCnfCode>*85</dtmfCnfCode>
    </mobility>
    <userId>Capital4</userId>
    <phoneServices useHTTPS="true">
    <provisioning>2</provisioning>
    <phoneService type="2" category="0">
    <name>Voicemail</name>
    <url>Application:Cisco/Voicemail</url>
    <vendor/>
    <version/>
    </phoneService>
    <phoneService type="0" category="0">
    <name>Missed Calls</name>
    <url>Application:Cisco/MissedCalls</url>
        <vendor/>
        <version/>
    </phoneService>
    <phoneService type="0" category="0">
    <name>Received Calls</name>
    <url>Application:Cisco/ReceivedCalls</url>
    <vendor/>
    <version/>
    </phoneService>
    <phoneService type="0" category="0">
    <name>Placed Calls</name>
    <url>Application:Cisco/PlacedCalls</url>
    <vendor/>
    <version/>
    </phoneService>
    <phoneService type="0" category="0">
    <name>Personal Directory</name>
    <url/>
    <vendor/>
    <version/>
    </phoneService>
    <phoneService type="0" category="0">
    <name>Corporate Directory</name>
    <url><directoryURL></directoryURL></url>
    <vendor/>
    <version/>
    </phoneService>
    </phoneServices>


    </device>
        '''
        cp_8865 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
    <sshUserId>cisco</sshUserId>
    <sshPassword>cisco</sshPassword>
    <sshAccess>0</sshAccess>
    <sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>j9-tzdata.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
        <ntps>
            <ntp>
                <name>%NTP%</name>
            <ntpMode>Unicast</ntpMode>
            </ntp>
        </ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<address></address>
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>false</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
            <authName>%RAMAL%</authName> 
            <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber>%RAMAL%</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact>%RAMAL%</contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
            <authName></authName>
            <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="3" lineIndex="3">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
            <authName></authName>
            <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>




</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>sip8845_65.12-5-1SR1-4</loadInformation>

<vendorConfig>
    <defaultWallpaperFile></defaultWallpaperFile>
    <disableSpeaker>false</disableSpeaker>
    <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
    <enableMuteFeature>false</enableMuteFeature>
    <enableGroupListen>true</enableGroupListen>
    <holdResumeKey>1</holdResumeKey>
    <recentsSoftKey>1</recentsSoftKey>
    <dfBit>1</dfBit>
    <pcPort>0</pcPort>
    <spanToPCPort>1</spanToPCPort>
    <garp>0</garp>
    <rtcp>1</rtcp>
    <videoRtcp>1</videoRtcp>
    <voiceVlanAccess>0</voiceVlanAccess>
    <videoCapability>1</videoCapability>
    <hideVideoByDefault>0</hideVideoByDefault>
    <separateMute>0</separateMute>
    <ciscoCamera>1</ciscoCamera>
    <usb1>1</usb1>
    <usb2>1</usb2>
    <usbClasses>0,1,2</usbClasses>
    <sdio>1</sdio>
    <wifi>1</wifi>
    <bluetooth>1</bluetooth>
    <bluetoothProfile>0,1</bluetoothProfile>
    <btpbap>0</btpbap>
    <bthfu>0</bthfu>
    <ehookEnable>0</ehookEnable>
    <autoSelectLineEnable>1</autoSelectLineEnable>
    <autoCallSelect>1</autoCallSelect>
    <incomingCallToastTimer>10</incomingCallToastTimer>
    <dialToneFromReleaseKey>0</dialToneFromReleaseKey>
    <joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
    <minimumRingVolume></minimumRingVolume>
    <simplifiedNewCall>0</simplifiedNewCall>
    <actionableAlert>0</actionableAlert>
    <showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
    <kemOneColumn>0</kemOneColumn>
    <lineMode>0</lineMode>
    <allCallsOnPrimary>0</allCallsOnPrimary>
    <softKeyControl>0</softKeyControl>
    <settingsAccess>1</settingsAccess>
    <webProtocol>0</webProtocol>
    <webAccess>0</webAccess>
    <webAdmin>1</webAdmin>
    <adminPassword></adminPassword>
    <sshAccess>0</sshAccess>
    <detectCMConnectionFailure>0</detectCMConnectionFailure>
    <g722CodecSupport>1</g722CodecSupport>
    <handsetWidebandEnable>2</handsetWidebandEnable>
    <headsetWidebandEnable>2</headsetWidebandEnable>
    <headsetWidebandUIControl>1</headsetWidebandUIControl>
    <handsetWidebandUIControl>1</handsetWidebandUIControl>
    <daysDisplayNotActive>1,7</daysDisplayNotActive>
    <displayOnTime>08:00</displayOnTime>
    <displayOnDuration>10:00</displayOnDuration>
    <displayIdleTimeout>00:10</displayIdleTimeout>
    <displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
    <displayRefreshRate>0</displayRefreshRate>
    <daysBacklightNotActive>1,7</daysBacklightNotActive>
    <backlightOnTime>08:00</backlightOnTime>
    <backlightOnDuration>10:00</backlightOnDuration>
    <backlightIdleTimeout>00:10</backlightIdleTimeout>
    <backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
    <recordingTone>0</recordingTone>
    <recordingToneLocalVolume>100</recordingToneLocalVolume>
    <recordingToneRemoteVolume>50</recordingToneRemoteVolume>
    <recordingToneDuration></recordingToneDuration>
    <moreKeyReversionTimer>5</moreKeyReversionTimer>
    <peerFirmwareSharing>0</peerFirmwareSharing>
    <loadServer></loadServer>
    <problemReportUploadURL></problemReportUploadURL>
    <enableCdpSwPort>1</enableCdpSwPort>
    <enableCdpPcPort>0</enableCdpPcPort>
    <enableLldpSwPort>1</enableLldpSwPort>
    <enableLldpPcPort>0</enableLldpPcPort>
    <cdpEnable>true</cdpEnable>
    <outOfRangeAlert>0</outOfRangeAlert>
    <scanningMode>2</scanningMode>
    <applicationURL></applicationURL>
    <appButtonTimer>0</appButtonTimer>
    <appButtonPriority>0</appButtonPriority>
    <specialNumbers></specialNumbers>
    <sendKeyAction>0</sendKeyAction>
    <powerOffWhenCharging>0</powerOffWhenCharging>
    <homeScreen>0</homeScreen>
    <accessContacts>1</accessContacts>
    <accessFavorites>1</accessFavorites>
    <accessVoicemail>1</accessVoicemail>
    <accessApps>1</accessApps>
    </vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName>%ASTER%</processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
    <vendor></vendor>
    <version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
        '''
        cp_9845 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
    <sshUserId>cisco</sshUserId>
    <sshPassword>cisco</sshPassword>
    <sshAccess>0</sshAccess>
    <sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>TzDataCSV.csv</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
        <ntps>
            <ntp>
                <name>%NTP%</name>
            <ntpMode>Unicast</ntpMode>
            </ntp>
        </ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<!--address>VSS.tropiconet.com</address-->
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>true</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
            <authName>%RAMAL%</authName> 
            <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber>2121017921</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact>2121017921</contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>4</busyTrigger>
</line>

<line  button="2" >
<featureID>2</featureID>
<featureLabel>Rapida00</featureLabel>
<speedDialNumber>0#</speedDialNumber>
</line>

<line  button="3">
<featureID>2</featureID>
<featureLabel>Rapida01</featureLabel>
<speedDialNumber>1#</speedDialNumber>
</line>
<line  button="4">
<featureID>2</featureID>
<featureLabel>Rapida02</featureLabel>
<speedDialNumber>2#</speedDialNumber>
</line>

</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>SIP894x.9-4-2SR3-1</loadInformation>
<vendorConfig>
    <defaultWallpaperFile></defaultWallpaperFile>
    <disableSpeaker>false</disableSpeaker>
    <disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
    <enableMuteFeature>false</enableMuteFeature>
    <enableGroupListen>true</enableGroupListen>
    <holdResumeKey>1</holdResumeKey>
    <recentsSoftKey>1</recentsSoftKey>
    <dfBit>1</dfBit>
    <pcPort>0</pcPort>
    <spanToPCPort>1</spanToPCPort>
    <garp>0</garp>
    <rtcp>1</rtcp>
    <videoRtcp>1</videoRtcp>
    <voiceVlanAccess>0</voiceVlanAccess>
    <videoCapability>1</videoCapability>
    <hideVideoByDefault>0</hideVideoByDefault>
    <separateMute>0</separateMute>
    <ciscoCamera>1</ciscoCamera>
    <usb1>1</usb1>
    <usb2>1</usb2>
    <usbClasses>0,1,2</usbClasses>
    <sdio>1</sdio>
    <wifi>1</wifi>
    <bluetooth>1</bluetooth>
    <bluetoothProfile>0,1</bluetoothProfile>
    <btpbap>0</btpbap>
    <bthfu>0</bthfu>
    <ehookEnable>0</ehookEnable>
    <autoSelectLineEnable>1</autoSelectLineEnable>
    <autoCallSelect>1</autoCallSelect>
    <incomingCallToastTimer>10</incomingCallToastTimer>
    <dialToneFromReleaseKey>0</dialToneFromReleaseKey>
    <joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
    <minimumRingVolume></minimumRingVolume>
    <simplifiedNewCall>0</simplifiedNewCall>
    <actionableAlert>0</actionableAlert>
    <showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
    <kemOneColumn>0</kemOneColumn>
    <lineMode>0</lineMode>
    <allCallsOnPrimary>0</allCallsOnPrimary>
    <softKeyControl>0</softKeyControl>
    <settingsAccess>1</settingsAccess>
    <webProtocol>0</webProtocol>
    <webAccess>0</webAccess>
    <webAdmin>1</webAdmin>
    <adminPassword></adminPassword>
    <sshAccess>0</sshAccess>
    <detectCMConnectionFailure>0</detectCMConnectionFailure>
    <g722CodecSupport>1</g722CodecSupport>
    <handsetWidebandEnable>2</handsetWidebandEnable>
    <headsetWidebandEnable>2</headsetWidebandEnable>
    <headsetWidebandUIControl>1</headsetWidebandUIControl>
    <handsetWidebandUIControl>1</handsetWidebandUIControl>
    <daysDisplayNotActive>1,7</daysDisplayNotActive>
    <displayOnTime>08:00</displayOnTime>
    <displayOnDuration>10:00</displayOnDuration>
    <displayIdleTimeout>00:10</displayIdleTimeout>
    <displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
    <displayRefreshRate>0</displayRefreshRate>
    <daysBacklightNotActive>1,7</daysBacklightNotActive>
    <backlightOnTime>08:00</backlightOnTime>
    <backlightOnDuration>10:00</backlightOnDuration>
    <backlightIdleTimeout>00:10</backlightIdleTimeout>
    <backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
    <recordingTone>0</recordingTone>
    <recordingToneLocalVolume>100</recordingToneLocalVolume>
    <recordingToneRemoteVolume>50</recordingToneRemoteVolume>
    <recordingToneDuration></recordingToneDuration>
    <moreKeyReversionTimer>5</moreKeyReversionTimer>
    <peerFirmwareSharing>0</peerFirmwareSharing>
    <loadServer></loadServer>
    <problemReportUploadURL></problemReportUploadURL>
    <enableCdpSwPort>1</enableCdpSwPort>
    <enableCdpPcPort>0</enableCdpPcPort>
    <enableLldpSwPort>1</enableLldpSwPort>
    <enableLldpPcPort>0</enableLldpPcPort>
    <cdpEnable>true</cdpEnable>
    <outOfRangeAlert>0</outOfRangeAlert>
    <scanningMode>2</scanningMode>
    <applicationURL></applicationURL>
    <appButtonTimer>0</appButtonTimer>
    <appButtonPriority>0</appButtonPriority>
    <specialNumbers></specialNumbers>
    <sendKeyAction>0</sendKeyAction>
    <powerOffWhenCharging>0</powerOffWhenCharging>
    <homeScreen>0</homeScreen>
    <accessContacts>1</accessContacts>
    <accessFavorites>1</accessFavorites>
    <accessVoicemail>1</accessVoicemail>
    <accessApps>1</accessApps>
    </vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt_BR</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<TLSResumptionTimer>3600</TLSResumptionTimer>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>1</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName></processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
        '''
        gxp_1615 = '''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Grandstream XML Provisioning Configuration -->
<gs_provision version="1">
    <config version="1">
    <!-- Forma de configuracao - TFTP -->
    <P212>0</P212>

    <!-- Sip Server -->
    <P47>%ASTER%</P47>

    <!-- Authenticate Password -->
    <P34>%PASS%</P34>

    <!-- SIP User ID -->
    <P35>%RAMAL%</P35>

    <!-- Authenticate ID -->
    <P36>%RAMAL%</P36>

    <!-- Nome do Ramal -->
    <P3>%NOME%</P3>

    <!--######### Account 2 ######## -->

    <!-- Authenticate Password -->
    <P406>%PASS2%</P406>

    <!-- SIP User ID -->
    <P404>%RAMAL2%</P404>

    <!-- Authenticate ID -->
    <P405>%RAMAL2%</P405>

    <!-- Account Display -->
    <P2480>1</P2480>

    <!-- Preferred Vocoder 1 - G.722 -->
    <P57>9</P57>

    <!-- Preferred Vocoder 2 - PCMA -->
    <P58>8</P58>

    <!-- NTP Server -->
    <P30>%NTP%</P30>

    <!-- Time Zone (-3) -->
    <P64>BRST+3</P64>

    <!-- Formato da data - dd-mm-yyyy -->
    <P102>2</P102>

    <!-- Formato da hora - 0-24h -->
    <P122>1</P122>

    <!-- Voice Vlan -->
    <P51></P51>

    <!-- Configuracao via TFTP -->
    <P212>0</P212>

    <!-- Caminho da configuracao no TFTP -->
    <P237>%TFTP%</P237>

    <!-- Linguagem -->
    <P1362>pt</P1362>

    <!-- Mostrar o User ID na tela -->
    <P2380>1</P2380>

    <!-- Admin password for web interface -->
    <P2>%WEB_PASS%</P2>

    <!-- Dial Plan -->
    <P290>{ ** | **x+ | x+ | #x+ | *#x+ }</P290>

    <!-- Ringtone -->
    <P104>3</P104>
    </config>
</gs_provision>
        '''
        gxp_2170 = '''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Grandstream XML Provisioning Configuration -->
<gs_provision version="1">
    <config version="1">
    <!-- Forma de configuracao - TFTP -->
    <P212>0</P212>

    <!-- Servidor de configuracao -->
    <P237>%TFTP%</P237>

    <!-- SIP Server -->
    <P47>%ASTER%</P47>

    <!-- Password -->
    <P34>%PASS%</P34>

    <!-- SIP User ID -->
    <P35>%RAMAL%</P35>

    <!-- Authenticate ID -->
    <P36>%RAMAL%</P36>

    <!-- Nome do Ramal -->
    <P3>%NOME%</P3>

    <!-- #############Conta SIP 2############### -->

    <!-- SIP Server -->
    <P402>%ASTER2%</P402>

    <!-- SIP User ID -->
    <P404>%RAMAL2%</P404>

    <!-- Authenticate ID -->
    <P405>%RAMAL2%</P405>

    <!-- Authenticate password -->
    <P406>%PASS2%</P406>    

    <!-- #############Conta SIP 3############### -->
    <!-- SIP Server -->
    <P502>%ASTER3%</P502>

    <!-- SIP User ID -->
    <P504>%RAMAL3%</P504>

    <!-- Authenticate ID -->
    <P505>%RAMAL3%</P505>

    <!-- Authenticate password -->
    <P506>%PASS3%</P506>

    <!-- Preferencia 1 de Codec - G.722 -->
    <P57>9</P57>

    <!-- Preferencia 2 de Codec - PCMA -->
    <P58>8</P58>

    <!-- NTP Server -->
    <P30>%NTP%</P30>

    <!-- Formato da data - dd-mm-yyyy -->
    <P102>2</P102>

    <!-- Mostrar data na barra superior -->
    <P8387>1</P8387>

    <!-- Formato da hora - 0-24h -->
    <P122>1</P122>

    <!-- Time Zone (-3) -->
    <P64>BRST+3</P64>

    <!-- Descanso de Tela -->
    <P2918>0</P2918>

    <!-- Desligar o bluetooth -->
    <P2910>0</P2910>

    <!-- Wallpaper download -->
    <P2916>1</P2916>

    <!-- Caminho do wallpaper -->
    <P2917>tftp://%TFTP%/wp2170.jpg</P2917>

    <!-- Voice Vlan -->
    <P51></P51>

    <!-- Linguagem -->
    <P1362>pt</P1362>

    <!-- Admin password for web interface -->
    <P2>%WEB_PASS%</P2>

    <!-- Dial Plan -->
    <P290>{ ** | **x+ | x+ | #x+ | *#x+ }</P290>

    <!-- Previsao do tempo -->
    <P1402>0</P1402>

    </config>
</gs_provision>
        '''
        yealink_22p = '''#!version:1.0.0.1
#File header "#!version:1.0.0.1" cannot be edited or deleted.##
#Line1 settings
#Activate/Deactivate the account1, 0-Disabled (Default), 1-Enabled
account.1.enable = %enable1%
#Configure the label of account1 which will display on the LCD screen
account.1.label = %name%
#Configure the display name of account1
account.1.display_name = %name%
#Configure the user name and password for register authentication
account.1.auth_name = %linha1%
account.1.password = %pass1%
#Configure the register user name
account.1.user_name = %linha1%
#Configure the SIP server address and port (5060 by default)
account.1.sip_server_host = %asterisk1%
account.1.sip_server_port = 5060
#Line2 settings
#Activate/Deactivate account2, 0-Disabled(Default), 1-Enabled
account.2.enable = %enable2%
#Configure the label of account2 which will display on the LCD screen
account.2.label =
#Configure the display name of account2
account.2.display_name =
#Configure the user name and password for register authentication
account.2.auth_name = %linha2%
account.2.password = %pass2%
#Configure the register user name
account.2.user_name = %linha2%
#Configure the SIP server address and port(5060 by default)
account.2.sip_server_host = %asterisk2%
account.2.sip_server_port = 5060
#Line3 settings
#Activate/Deactivate the account3, 0-Disabled(Default), 1-Enabled
account.3.enable = %enable3%
#Configure the label of account3 which will display on the LCD screen
account.3.label =
#Configure the display name of account3
account.3.display_name =
#Configure the user name and password for register authentication
account.3.auth_name = %linha3%
account.3.password = %pass3%
#Configure the register user name
account.3.user_name = %linha3%
#Configure the SIP server address and port (5060 by default)
account.3.sip_server_host = %asterisk3%
account.3.sip_server_port = 5060
#Configure the NTP Server
local_time.ntp_server1 = %ntp%
local_time.time_zone = -3
local_time.time_zone_name = Brazil(DST)
        '''

        #Entrada de Dados
        os.system('clear')
        opcao_menu =input('Para prosseguir, é necessário que uma planilha esteja no formato "AP.xlsx"\
e que tenha a página nomeada como AP.\n\nPressione qualquer tecla para continuar...')
        os.system('clear')
        ip_asterisk = input("Qual o IP do asterisk? ")
        ip_ntp = input('Qual o Ip do NTP? ')
        pass_asterisk = input("Qual a senha de registro dos telefones? ")
        check_tel = input("Vão ser configurados telefones GrandStream? (s ou n): ")


        if check_tel == 's':
           ip_tftp = input('Qual o IP do TFTP? ')
           pass_web = input('Qual senha será utilizada para acesso WEB dos telefones? ')

        # Abrindo Planilha e Página
        workbook = openpyxl.load_workbook('/srv/tftp/AP.xlsx')
        sheet_alunos = workbook['AP']

        for indice, linha in enumerate(sheet_alunos.iter_rows(min_row=2)):

               modelo = linha[0].value
               modelo = modelo.lower()
               if modelo not in lista_modelos:
                   print(f'O modelo {modelo} não é válido')
                   continue
               mac_ramal = linha[1].value
               mac_ramal = str(mac_ramal)
               mac_ramal = correcao_mac(mac_ramal)
               num_linha1 = linha[2].value
            #   num_linha2 = linha[4].value
               num_linha2 = ''
            #   num_linha3 = linha[5].value
               num_linha3 = ''
               nome_ramal = linha[3].value
               num_linha1_bool = bool(num_linha1)
            #   num_linha2_bool = bool(num_linha2)
               num_linha2_bool = None
            #   num_linha3_bool = bool(num_linha3)
               num_linha3_bool = None

               try:
                   if num_linha1_bool == True:


                       if modelo == 'gxp2170':
                           new_name = mac_ramal.lower()
                           new_name = '/srv/tftp/cfg' + new_name + '.xml'
                           new_name = new_name.replace(' ','')

                           shell(f'touch {new_name}')
                           write_text(new_name, gxp_2170)

                           replace_pat(new_name, '%NTP%', str(ip_ntp))
                           replace_pat(new_name, '%TFTP%', str(ip_tftp))
                           replace_pat(new_name, '%WEB_PASS%', str(pass_web))


                           if num_linha1_bool == True:
                               replace_pat(new_name, '%RAMAL%', str(num_linha1))
                               replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                               replace_pat(new_name, '%PASS%', str(pass_asterisk))

                               if bool(nome_ramal) == True:
                                   replace_pat(new_name, '%NOME%', nome_ramal)
                               else:
                                   replace_pat(new_name, '%NOME%', '')


                           else:
                               replace_pat(new_name, '%RAMAL%', '')
                               replace_pat(new_name, '%NOME%', '')
                               replace_pat(new_name, '%ASTER%', '')
                               replace_pat(new_name, '%PASS%', '')


                           if num_linha2_bool == True:
                               replace_pat(new_name, '%RAMAL2%', str(num_linha2))
                               replace_pat(new_name, '%ASTER2%', str(ip_asterisk))
                               replace_pat(new_name, '%PASS2%', str(pass_asterisk))


                           else:
                               replace_pat(new_name, '%RAMAL2%', '')
                               replace_pat(new_name, '%NOME2%', '')
                               replace_pat(new_name, '%ASTER2%', '')
                               replace_pat(new_name, '%PASS2%', '')


                           if num_linha3_bool == True:
                               replace_pat(new_name, '%RAMAL3%', str(num_linha3))
                               replace_pat(new_name, '%ASTER3%', str(ip_asterisk))
                               replace_pat(new_name, '%PASS3%', str(pass_asterisk))


                           else:
                               replace_pat(new_name, '%RAMAL3%', '')
                               replace_pat(new_name, '%ASTER3%', '')
                               replace_pat(new_name, '%PASS3%', '')




                       elif modelo == 'gxp1615':
                           if bool(mac_ramal) == True:
                               new_name = mac_ramal.lower()
                               new_name = '/srv/tftp/cfg' + new_name + '.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, gxp_1615)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))
                               replace_pat(new_name, '%TFTP%', str(ip_tftp))
                               replace_pat(new_name, '%WEB_PASS%', str(pass_web))


                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))


                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')


                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%NOME%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')


                               if num_linha2 == True:
                                   replace_pat(new_name, '%RAMAL2%', str(num_linha2))
                                   replace_pat(new_name, '%PASS2%', pass_asterisk)
                               else:
                                   replace_pat(new_name, '%RAMAL2%', '')
                                   replace_pat(new_name, '%PASS2%', '')
                           else:
                               print('* * * * Não Existe MAC associado * * * *')


                       elif modelo == 'gxp1625':
                           if bool(mac_ramal) == True:
                               new_name = mac_ramal.lower()
                               new_name = '/srv/tftp/cfg'  + new_name + '.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, gxp_1615)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))
                               replace_pat(new_name, '%TFTP%', str(ip_tftp))
                               replace_pat(new_name, '%WEB_PASS%', str(pass_web))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')


                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%NOME%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')


                               if num_linha2 == True:
                                   replace_pat(new_name, '%RAMAL2%', str(num_linha2))
                                   replace_pat(new_name, '%PASS2%', pass_asterisk)
                               else:
                                   replace_pat(new_name, '%RAMAL2%', '')
                                   replace_pat(new_name, '%PASS2%', '')
                           else:
                               print('* * * * Não Existe MAC associado * * * *')


                       elif modelo == 't22p':
                           new_name = mac_ramal.lower()
                           new_name = '/srv/tftp' + new_name + '.cfg'
                           new_name = new_name.replace(' ','')

                           shell(f'touch {new_name}')
                           write_text(new_name, yealink_22p)
                           replace_pat(new_name, '%ntp%', str(ip_ntp))


                           if num_linha1_bool == True:
                               replace_pat(new_name,'%enable1%', '1')
                               replace_pat(new_name, '%linha1%', str(num_linha1))
                               replace_pat(new_name, '%asterisk1%', str(ip_asterisk))
                               replace_pat(new_name, '%pass1%', str(pass_asterisk))

                               if bool(nome_ramal) == True:
                                   replace_pat(new_name, '%name%', nome_ramal)
                               else:
                                   replace_pat(new_name, '%name%', '')


                           else:
                               replace_pat(new_name, '%enable1%', '0')
                               replace_pat(new_name, '%name%', '')
                               replace_pat(new_name, '%linha1%', '')
                               replace_pat(new_name, '%asterisk1%', '')
                               replace_pat(new_name, '%pass1%', '')


                           if num_linha2_bool == True:
                               replace_pat(new_name,'%enable2%', '1')
                               replace_pat(new_name, '%linha2%', str(num_linha2))
                               replace_pat(new_name, '%asterisk2%', str(ip_asterisk))
                               replace_pat(new_name, '%pass2%', str(pass_asterisk))


                           else:
                               replace_pat(new_name, '%enable2%', '0')
                               replace_pat(new_name, '%linha2%', '')
                               replace_pat(new_name, '%asterisk2%', '')
                               replace_pat(new_name, '%pass2%', '')


                           if num_linha3_bool == True:
                               replace_pat(new_name,'%enable3%', '1')
                               replace_pat(new_name, '%linha3%', str(num_linha3))
                               replace_pat(new_name, '%asterisk3%', str(ip_asterisk))
                               replace_pat(new_name, '%pass3%', str(pass_asterisk))


                           else:
                               replace_pat(new_name, '%enable3%', '0')
                               replace_pat(new_name, '%linha3%', '')
                               replace_pat(new_name, '%asterisk3%', '')
                               replace_pat(new_name, '%pass3%', '')

                       elif modelo == 'cp-3905':
                           if bool(mac_ramal) == True:
                               new_name = mac_ramal.upper()
                               new_name = '/srv/tftp/SEP' + new_name + '.cnf.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, cp_3905)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)

                                   else:
                                       replace_pat(new_name, '%NOME%', '')

                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')
                                   replace_pat(new_name, '%NOME%', '')

                           else:
                               print('* * * * Não Existe MAC associado * * * *')

                       elif modelo == 'cp-7821':
                           if bool(mac_ramal) == True:
                               new_name = mac_ramal.upper()
                               new_name = '/srv/tftp/SEP' + new_name + '.cnf.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, cp_7821)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')

                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')
                                   replace_pat(new_name, '%NOME%', '')

                           else:
                               print('* * * * Não Existe MAC associado * * * *')



                       elif modelo == 'cp-8845':
                            if bool(mac_ramal) == True:
                               new_name = mac_ramal.upper()
                               new_name = '/srv/tftp/SEP' + new_name + '.cnf.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, cp_8845)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')

                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')
                                   replace_pat(new_name, '%NOME%', '')

                            else:
                               print('* * * * Não Existe MAC associado * * * *')

                       elif modelo == 'cp-8865':

                            if bool(mac_ramal) == True:
                               new_name = mac_ramal.upper()
                               new_name = '/srv/tftp/SEP' + new_name + '.cnf.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, cp_8865)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')


                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')
                                   replace_pat(new_name, '%NOME%', '')

                            else:
                               print('* * * * Não Existe MAC associado * * * *')


                       elif modelo == 'cp-7942':

                            if bool(mac_ramal) == True:
                               new_name = mac_ramal.upper()
                               new_name = '/srv/tftp/SEP' + new_name + '.cnf.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, cp_7942)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')

                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')
                                   replace_pat(new_name, '%NOME%', '')

                            else:
                               print('* * * * Não Existe MAC associado * * * *')

                       elif modelo == 'cp-9845':

                            if bool(mac_ramal) == True:
                               new_name = mac_ramal.upper()
                               new_name = '/srv/tftp/SEP' + new_name + '.cnf.xml'
                               new_name = new_name.replace(' ','')

                               shell(f'touch {new_name}')
                               write_text(new_name, cp_9845)

                               replace_pat(new_name, '%NTP%', str(ip_ntp))

                               if num_linha1_bool == True:
                                   replace_pat(new_name, '%RAMAL%', str(num_linha1))
                                   replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                                   replace_pat(new_name, '%PASS%', str(pass_asterisk))

                                   if bool(nome_ramal) == True:
                                       replace_pat(new_name, '%NOME%', nome_ramal)


                                   else:
                                       replace_pat(new_name, '%NOME%', '')


                               else:
                                   replace_pat(new_name, '%RAMAL%', '')
                                   replace_pat(new_name, '%ASTER%', '')
                                   replace_pat(new_name, '%PASS%', '')
                                   replace_pat(new_name, '%NOME%', '')

                            else:
                               print('* * * * Não Existe MAC associado * * * *')
                   else:
                       print(f'* * * * O MAC {mac_ramal} não possui ramal associado ou informação foi prenchida incorretamente * * * *')   

               except:
                   print('Fim da Planilha')
        for arquivo in os.listdir():
            if arquivo.endswith('.xml'):
                quant_arquivos += 1
            elif arquivo.endswith('.cfg'):
                quant_arquivos += 1
        print('\n* * * * Fim da Planilha! * * * *\n')
        print(f'* * * * Foram gerados {quant_arquivos} arquivos de configuração * * * *\n')
        if opcao_menu == 's':
            continue
        elif opcao_menu == 'n':
            break