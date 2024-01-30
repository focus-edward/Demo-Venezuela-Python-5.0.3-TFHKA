import tkinter as tk
from tkinter import filedialog
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtSerialPort import QSerialPortInfo

import sys
import TfhkaPyGD
import os
import time






class Principal(QMainWindow):

	def __init__(self):
		super().__init__()
		QDialog.__init__(self)
		QMainWindow.__init__(self)
		QToolButton.__init__(self)
		ui_file_path = os.path.join(os.path.dirname(__file__), 'DemoPython.ui')
		uic.loadUi(ui_file_path, self)
		self.printer = TfhkaPyGD.Tfhka()
		self.app = QApplication(sys.argv)




		self.pushports.clicked.connect(self.push_ports)
		self.btnabrir.clicked.connect(self.abrir_puerto)
		self.btncerrar.clicked.connect(self.cerrar_puerto)
		self.btnmodelopais.clicked.connect(self.modelo)
		self.btnenviar.clicked.connect(self.enviar_cmd)
		self.btnarchivo.clicked.connect(self.enviar_arc)
		self.btnestadoerror.clicked.connect(self.estado_error)
		self.btnimprimirZ.clicked.connect(self.imprimir_ReporteZ)
		self.btnimprimirX.clicked.connect(self.imprimir_ReporteX)
		self.btnestado.clicked.connect(self.obtener_estado)
		self.btnleerX.clicked.connect(self.obtener_reporteX)
		self.btnZnumero_imp.clicked.connect(self.ImpZpornumero)
		self.btnZfecha_imp.clicked.connect(self.ImpZporfecha)
		self.btnFactura.clicked.connect(self.factura)
		self.btnFacturaPer.clicked.connect(self.facturaper)
		self.btnFacturaIgtf.clicked.connect(self.facturaigtf)
		self.btnFacturaAnu.clicked.connect(self.facturaanu)
		self.btnDocNoFiscal.clicked.connect(self.documentoNF)
		self.btnNotaCredito.clicked.connect(self.notaCredito)
		self.btnNotaCreIgtf.clicked.connect(self.notaCreditoIgtf)
		self.btnNotaDebito.clicked.connect(self.notaDebito)
		self.btnreipmFact_numero.clicked.connect(self.ReimprimirFacturas)
		self.btnZnumero_obt.clicked.connect(self.ObtZpornumero)
		self.btnZfecha_obt.clicked.connect(self.ObtZporfecha)
		self.btnultZ_obt.clicked.connect(self.obtener_reporteZ)
		self.btnver_con.clicked.connect(self.btn_ver_con)
		self.status_arch.clicked.connect(self.estado_archivo)
		self.rep_arch.clicked.connect(self.reporte_archivo)
		self.btnextraerFact_numero.clicked.connect(self.ObtFactpornumero)
		self.ver_gaveta.clicked.connect(self.vergaveta)

		self.menuAcerca_de.aboutToShow.connect(self.acerca_de)




	def acerca_de (self):
		dialog = QDialog()
		ui_file_path = os.path.join(os.path.dirname(__file__), 'AboutDemopy.ui')
		uic.loadUi (ui_file_path, dialog)
		dialog.exec_()


	def push_ports(self):
		menu = QMenu(self.pushports)
		available_ports = QSerialPortInfo.availablePorts()
		
		for port_info in available_ports:
			# Verifica si el nombre del puerto comienza con "COM"
			if port_info.portName().startswith("COM"):
				action = QAction(port_info.portName(), self)
				action.triggered.connect(lambda checked, port=port_info: self.seleccionar_puerto(port))
				menu.addAction(action)
		
		menu.exec(self.pushports.mapToGlobal(self.pushports.rect().bottomLeft()))

		
	def seleccionar_puerto(self, port_info):
		self.pushports.setText(port_info.portName())		
		self.puerto_seleccionado = port_info.portName()  # Asigna el puerto seleccionado a la variable

	def obtener_puerto_seleccionado(self):
			return self.puerto_seleccionado

	def abrir_puerto(self):

		try:
			self.txt_informacion.setText("")
			puerto = self.obtener_puerto_seleccionado()
			resp = self.printer.OpenFpctrl(str(puerto))
			if resp:
				self.txt_informacion.setText("Impresora Conectada Correctamente en: " + puerto)
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
				self.ver_con.setText("Puerto Abierto")
			else:
				if self.printer.bandera:																			# Verifica si ya esta abierto el puerto
					self.txt_informacion.setText("Impresora Conectada Correctamente en: " + puerto)
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Puerto Abierto")
				else:
					self.txt_informacion.setText("Impresora no Conectada o Error Accediendo al Puerto")
					self.ver_con.setStyleSheet("background-color: rgb(231, 231, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Error Puerto")			
			
		except:
			self.txt_informacion.setText("Impresora no Conectada o Error Accediendo al Puerto")
			self.ver_con.setStyleSheet("background-color: rgb(231, 231, 0);color: black;font: 900 9pt;")
			self.ver_con.setText("Error Puerto")				

	def cerrar_puerto(self):
		self.txt_informacion.setText("")
		resp = self.printer.CloseFpctrl()
		if not resp:
			self.txt_informacion.setText("Impresora Desconectada")
			self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt;")
			self.ver_con.setText("Puerto Cerrado")
		else:
			self.txt_informacion.setText("Error")
			self.ver_con.setStyleSheet("background-color: red;color: white;font: 900 9pt;")
			self.ver_con.setText("Puerto Cerrado")			

	def vergaveta(self):
		resp=self.printer.SendCmd("0")
		time.sleep(1.5)
		if not resp:
			self.txt_informacion.setText("No tiene una gaveta conectada.")
			self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt;")
			self.ver_con.setText("Verificar Gaveta")
		else:
			self.txt_informacion.setText("Apertura de gaveta")
			self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
			self.ver_con.setText("Verificar gaveta")				


	def modelo(self):
		mod = "SV"
		try:
			mod = self.printer.GetSVPrinterData()			
			modelo = mod._pmodel

			match modelo: 	
				case "Z1F":
					modelo = "BIXOLON SRP-812"
				case "Z7C":
					modelo = "FISCAT HKA80"
				case "Z1B":
					modelo = "BIXOLON SRP-350"
				case "ZZH":
					modelo = "ACLAS PP9"
				case "Z6C":
					modelo = "DASCOM TALLY 1140"
				case "Z6A":
					modelo = "DASCOM TALLY 1125"
				case "Z6B":
					modelo = "DASCOM DT-230"
				case "ZZP":
					modelo = "ACLAS PP9-PLUS"		
				case "Z7A":
					modelo = "FISCAT HKA-112"
				case "Z1E":
					modelo = "BIXOLON SRP-280"
				case "ZPA":
					modelo = "STAR HSP-7000"													
				case _:
					modelo = "Modelo Desconocido"

			VE = mod._pcountry
			match VE:
				case "VE":
					VE = "VENEZUELA"
				case _:
					VE = "Desconocido"

			if modelo != "Modelo Desconocido" and VE != "Desconocido":
				salida = f"============== SV ==============\nMarca y Modelo de la impresora: {modelo}\nPais de la impresora: {VE}"
				self.txt_informacion.setText(salida)
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
				self.ver_con.setText("Modelo y Pais")
			else:
				salida = f"============== SV ==============\nMarca y Modelo de la impresora: {modelo}\nPais de la impresora: {VE}"
				self.txt_informacion.setText(salida)
				self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt;")
				self.ver_con.setText("Modelo y Pais")	
		except:
			self.txt_informacion.setText("Impresora No Conectada")
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 9pt;")
			self.ver_con.setText("Modelo y Pais")


	def enviar_cmd(self):
		try:	
			cmd = self.txt_cmd.text()
			sendcmd=self.printer.SendCmd(str(cmd))
			if sendcmd:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
				self.ver_con.setText("Comando enviado")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
				self.ver_con.setText("Comando no enviado")	
		except:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Enviar Comando")		
			self.txt_informacion.setText("Impresora No Conectada")		



	def enviar_arc(self):
		cmd = filedialog.askopenfilename()
		match cmd:

			case "":
				self.ver_con.setStyleSheet("background-color: white;color: black;font: 900 7pt")
				self.ver_con.setText("No procesado")
				salida= "Usted no selecciono un archivo"
				self.txt_informacion.setText(salida)
			
			case _:

				if self.printer.bandera:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
					self.ver_con.setText("Comando enviado")
					self.printer.SendCmdFile(cmd)
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
					self.ver_con.setText("Comando no enviado")	
				

	def estado_error(self):
		try:
			self.txt_informacion.setText("")
			self.estado = self.printer.ReadFpStatus()
			STATUSDESC = self.estado[0:2]
			status_descrip = self.status_description(STATUSDESC)
			self.txt_informacion.setText("Estado: " + self.estado[0:2] + "\nDescripcion de estado: "+ status_descrip +"\n" + "Error: " + self.estado[5:9] + "\nDescripcion del Error: "+ self.estado[11:])		
			if not self.printer.bandera:
				self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
				self.ver_con.setText("Estado y Error")		
				self.txt_informacion.setText("Impresora No Conectada")
			else:	
				match self.estado[0]:
					case _:
						if self.estado:
							self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
							self.ver_con.setText("Estado y Error")
						else:
							self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
							self.ver_con.setText("Estado y Error")	

		except Exception as e:
			print (str(e))
			salida= "Codigo de error: 137"
			salida+= "\nMensaje de error: No hay respuesta"
			salida+= "\nCodigo de Status: 0"	
			salida+= "\nDescripcion del estatus: Estado Desconocido"					
			self.txt_informacion.setText(salida)
			self.ver_con.setStyleSheet("background-color: rgb(231, 231, 0);color: black;font: 900 7pt;")
			self.ver_con.setText("Estado Desconocido")					
					

	def btn_ver_con(self):																		# Verificar estado de conexion
		self.estado = self.printer.bandera
		try:
			if self.estado:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
				self.ver_con.setText("Conexion OK")
				self.txt_informacion.setText("")
				self.estado = self.printer.ReadFpStatus()

			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
				self.ver_con.setText("No Conect.")		

		except:
			salida= "Codigo de error: 137"
			salida+= "\nMensaje de error: No hay respuesta"
			salida+= "\nCodigo de Status: 0"	
			salida+= "\nDescripcion del estatus: Estado Desconocido"					
			self.txt_informacion.setText(salida)
			self.ver_con.setStyleSheet("background-color: rgb(231, 231, 0);color: black;font: 900 7pt;")
			self.ver_con.setText("Estado Desconocido")			


			

	def imprimir_ReporteZ(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Imp. Reporte Z")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:						
			printzreport=self.printer.PrintZReport()
			contador = 1
			while printzreport == None and contador < 6:
				time.sleep(1)
				contador += 1
			if printzreport:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
				self.ver_con.setText("Reporte Z")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
				self.ver_con.setText("Reporte Z")				

	def imprimir_ReporteX(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Imp. Reporte X")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:			
			printxreport=self.printer.PrintXReport()
			contador = 1
			while printxreport == None and contador < 6:
				time.sleep(1)
				contador += 1
			if printxreport:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
				self.ver_con.setText("Reporte X")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
				self.ver_con.setText("Reporte X")	

	def obtener_estado(self):
		estado = str(self.cmbestado.currentText())
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Enviar Comando")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:	
			if estado == "S1":
				estado_s1 = self.printer.GetS1PrinterData()
				salida= "==============Estado S1==============\n"
				salida+= "\nNúmero de cajero activo: " + str(estado_s1._cashierNumber)
				salida+= "\nMonto total de ventas diarias: " + str(estado_s1._totalDailySales)
				salida+= "\nNúmero de la última factura: " + str(estado_s1._lastInvoiceNumber)
				salida+= "\nCantidad de facturas en el día: " + str(estado_s1._quantityOfInvoicesToday)
				salida+= "\nNumero de la última nota de débito: " + str(estado_s1._lastDebtNoteNumber)
				salida+= "\nCantidad de notas de débito en el día: " + str(estado_s1._quantityDebtNoteToday)
				salida+= "\nNúmero de la última nota de crédito: " + str(estado_s1._lastNCNumber)
				salida+= "\nCantidad de notas de crédito en el día: " + str(estado_s1._quantityOfNCToday)
				salida+= "\nNumero del último documento no fiscal: " + str(estado_s1._numberNonFiscalDocuments)
				salida+= "\nCantidad de documentos no fiscales: " + str(estado_s1._quantityNonFiscalDocuments)
				salida+= "\nCantidad de reportes fiscales: " + str(estado_s1._fiscalReportsCounter)
				salida+= "\nContador de cierre diario (Reporte Z): " + str(estado_s1._dailyClosureCounter)
				salida+= "\nRIF de fiscalización de la impresora: " + str(estado_s1._rif)
				salida+= "\nNúmero de registro de la impresora fiscal: " + str(estado_s1._registeredMachineNumber)
				salida+= "\nHora actual de la impresora: " + str(estado_s1._currentPrinterTime)
				salida+= "\nFecha actual de la impresora: " + str(estado_s1._currentPrinterDate)
				self.txt_informacion.setText(salida)
				if estado_s1:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S1")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S1")				

			if estado == "S2":
				estado_s2 = self.printer.GetS2PrinterData()
				salida= "==============Estado S2==============\n"
				salida+= "\nSubtotal de BI: "+ str(estado_s2._subTotalBases)
				salida+= "\nSubtotal de Impuesto: " + str(estado_s2._subTotalTax)
				salida+= "\nInformación IGTF: " + str(estado_s2._dataDummy)
				salida+= "\nCantidad de articulos: " + str(estado_s2._quantityArticles)
				salida+= "\nMonto por Pagar: " + str(estado_s2._amountPayable)
				salida+= "\nNumero de Pagos Realizados: " + str(estado_s2._numberPaymentsMade)
				salida+= "\nTipo de Documento: " + str(estado_s2._typeDocument)
				self.txt_informacion.setText(salida)
				if estado_s2:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S2")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S2")		


			if estado == "S3":
				estado_s3 = self.printer.GetS3PrinterData()
				salida= "---Estado S3---\n"
				salida+= "\nTipo Tasa 1 (1 = Incluido, 2= Excluido): "+ str(estado_s3._typeTax1)
				salida+= "\nValor Tasa 1: "+ str(estado_s3._tax1) + " %"
				salida+= "\nTipo Tasa 2 (1 = Incluido, 2= Excluido): " + str(estado_s3._typeTax2)
				salida+= "\nValor Tasa2: " + str(estado_s3._tax2) + " %"
				salida+= "\nTipo Tasa 3 (1 = Incluido, 2= Excluido): " + str(estado_s3._typeTax3)
				salida+= "\nValor Tasa 3: " + str(estado_s3._tax3) + " %"
				salida+= "\nTipo IGTF (1 = Incluido, 2= Excluido): " + str(estado_s3._typeIgtf)
				salida+= "\nValor IGTF: " + str(estado_s3._igtf) + " %"
				dataflag=(estado_s3._systemFlags)
				salida += "\n\nLista de Flags:\n"
				for i in range(64):
					salida += "[{:02d}] = {}\n".format(i, dataflag[i])
				self.txt_informacion.setText(salida)
				if estado_s3:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S3")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S3")					

			if estado == "S4":
				estado_s4 = self.printer.GetS4PrinterData()
				salida= "---Estado S4---"
				salida+= "\nMontos en Medios de Pago:\n " + str(estado_s4._allMeansOfPayment)
				self.txt_informacion.setText(salida)
				if estado_s4:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S4")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S4")					

			if estado == "S5":
				estado_s5 = self.printer.GetS5PrinterData()
				salida= "---Estado S5---\n"
				salida+= "\nNumero de RIF: "+ str(estado_s5._rif)
				salida+= "\nNumero de Registro: " + str(estado_s5._registeredMachineNumber)
				salida+= "\nNumero de Memoria de Auditoria : " + str(estado_s5._auditMemoryNumber)
				salida+= "\nCapacidad Total de Memoria Auditoria: " + str(estado_s5._auditMemoryTotalCapacity) + " MB"
				salida+= "\nEspacio Disponible: " + str(estado_s5._auditMemoryFreeCapacity) + " MB"
				salida+= "\nCantidad Documentos Registrados: " + str(estado_s5._numberRegisteredDocuments)
				self.txt_informacion.setText(salida)
				if estado_s5:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S5")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S5")					

			if estado == "S6":
				estado_s6 = self.printer.GetS6PrinterData()
				salida= "---Estado S6---\n"
				salida+= "\nModo Facturacion: "+ str(estado_s6._bit_Facturacion)
				salida+= "\nModo Slip: " + str(estado_s6._bit_Slip)
				salida+= "\nModo Validacion: " + str(estado_s6._bit_Validacion)
				self.txt_informacion.setText(salida)

	def estado_archivo (self):
		estado = str(self.status_s.currentText())	
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Estado a Archivo")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:	
			if estado == "S1":
				estado_s1 = self.printer.GetS1PrinterData()
				salida= "==============Estado S1==============\n"
				salida+= "\nNúmero de cajero activo: " + str(estado_s1._cashierNumber)
				salida+= "\nMonto total de ventas diarias: " + str(estado_s1._totalDailySales)
				salida+= "\nNúmero de la última factura: " + str(estado_s1._lastInvoiceNumber)
				salida+= "\nCantidad de facturas en el día: " + str(estado_s1._quantityOfInvoicesToday)
				salida+= "\nNumero de la última nota de débito: " + str(estado_s1._lastDebtNoteNumber)
				salida+= "\nCantidad de notas de débito en el día: " + str(estado_s1._quantityDebtNoteToday)
				salida+= "\nNúmero de la última nota de crédito: " + str(estado_s1._lastNCNumber)
				salida+= "\nCantidad de notas de crédito en el día: " + str(estado_s1._quantityOfNCToday)
				salida+= "\nNumero del último documento no fiscal: " + str(estado_s1._numberNonFiscalDocuments)
				salida+= "\nCantidad de documentos no fiscales: " + str(estado_s1._quantityNonFiscalDocuments)
				salida+= "\nCantidad de reportes fiscales: " + str(estado_s1._fiscalReportsCounter)
				salida+= "\nContador de cierre diario (Reporte Z): " + str(estado_s1._dailyClosureCounter)
				salida+= "\nRIF de fiscalización de la impresora: " + str(estado_s1._rif)
				salida+= "\nNúmero de registro de la impresora fiscal: " + str(estado_s1._registeredMachineNumber)
				salida+= "\nHora actual de la impresora: " + str(estado_s1._currentPrinterTime)
				salida+= "\nFecha actual de la impresora: " + str(estado_s1._currentPrinterDate)
				if estado_s1:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S1")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S1")				

			if estado == "S2":
				estado_s2 = self.printer.GetS2PrinterData()
				salida= "==============Estado S2==============\n"
				salida+= "\nSubtotal de BI: "+ str(estado_s2._subTotalBases)
				salida+= "\nSubtotal de Impuesto: " + str(estado_s2._subTotalTax)
				salida+= "\nInformación IGTF: " + str(estado_s2._dataDummy)
				salida+= "\nCantidad de articulos: " + str(estado_s2._quantityArticles)
				salida+= "\nMonto por Pagar: " + str(estado_s2._amountPayable)
				salida+= "\nNumero de Pagos Realizados: " + str(estado_s2._numberPaymentsMade)
				salida+= "\nTipo de Documento: " + str(estado_s2._typeDocument)
				if estado_s2:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S2")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S2")		


			if estado == "S3":
				try:
					estado_s3 = self.printer.GetS3PrinterData()
					salida= "---Estado S3---\n"
					salida+= "\nTipo Tasa 1 (1 = Incluido, 2= Excluido): "+ str(estado_s3._typeTax1)
					salida+= "\nValor Tasa 1: "+ str(estado_s3._tax1) + " %"
					salida+= "\nTipo Tasa 2 (1 = Incluido, 2= Excluido): " + str(estado_s3._typeTax2)
					salida+= "\nValor Tasa2: " + str(estado_s3._tax2) + " %"
					salida+= "\nTipo Tasa 3 (1 = Incluido, 2= Excluido): " + str(estado_s3._typeTax3)
					salida+= "\nValor Tasa 3: " + str(estado_s3._tax3) + " %"
					salida+= "\nTipo IGTF (1 = Incluido, 2= Excluido): " + str(estado_s3._typeIgtf)
					salida+= "\nValor IGTF: " + str(estado_s3._igtf) + " %"
					dataflag=(estado_s3._systemFlags)
					salida += "\n\nLista de Flags:\n"
					for i in range(64):
						salida += "[{:02d}] = {}\n".format(i, dataflag[i])
					if estado_s3:
						self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
						self.ver_con.setText("Reporte S3")
					else:
						self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
						self.ver_con.setText("Reporte S3")			
				except:
						self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
						self.ver_con.setText("Reporte S3")	
						salida= "No se pudo extraer informacion..."

			if estado == "S4":
				try:
					estado_s4 = self.printer.GetS4PrinterData()
					salida= "---Estado S4---"
					salida+= "\nMontos en Medios de Pago:\n " + str(estado_s4._allMeansOfPayment)
					if estado_s4:
						self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
						self.ver_con.setText("Reporte S4")
					else:
						self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
						self.ver_con.setText("Reporte S4")	
				except:
						self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
						self.ver_con.setText("Reporte S4")
						salida= "No se pudo extraer informacion..."										

			if estado == "S5":
				estado_s5 = self.printer.GetS5PrinterData()
				salida= "---Estado S5---\n"
				salida+= "\nNumero de RIF: "+ str(estado_s5._rif)
				salida+= "\nNumero de Registro: " + str(estado_s5._registeredMachineNumber)
				salida+= "\nNumero de Memoria de Auditoria : " + str(estado_s5._auditMemoryNumber)
				salida+= "\nCapacidad Total de Memoria Auditoria: " + str(estado_s5._auditMemoryTotalCapacity) + " MB"
				salida+= "\nEspacio Disponible: " + str(estado_s5._auditMemoryFreeCapacity) + " MB"
				salida+= "\nCantidad Documentos Registrados: " + str(estado_s5._numberRegisteredDocuments)
				if estado_s5:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Reporte S5")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 9pt")
					self.ver_con.setText("Reporte S5")					

			if estado == "S6":
				estado_s6 = self.printer.GetS6PrinterData()
				salida= "---Estado S6---\n"
				salida+= "\nModo Facturacion: "+ str(estado_s6._bit_Facturacion)
				salida+= "\nModo Slip: " + str(estado_s6._bit_Slip)
				salida+= "\nModo Validacion: " + str(estado_s6._bit_Validacion)
			root = tk.Tk()
			root.withdraw()
			nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
			if nombre_archivo:
				# Abre el archivo en modo de escritura ('w')
				with open(nombre_archivo, 'w') as archivo:
					# Escribe cada línea en el archivo
					for linea in salida:
						archivo.write(linea)  # Agrega un salto de línea al final de cada línea
				print(f"Se ha guardado el archivo en: {nombre_archivo}")
			else:
				print("No se ha seleccionado ninguna ubicación para guardar el archivo.")


	def obtener_reporteZ(self):
		if self.printer.bandera:
				try:
					reporte = self.printer.GetZReport()
					salida= "---EXTRACCIÓN DE REPORTE Z---\n"
					salida+= "\nNumero Ultimo Reporte Z: "+ str(reporte._numberOfLastZReport)
					salida+= "\nFecha Ultimo Reporte Z: "+ str(reporte._zReportDate)
					salida+= "\nHora Ultimo Reporte Z: "+ str(reporte._zReportTime)
					salida+= "\nNumero Ultima Factura: "+ str(reporte._numberOfLastInvoice)
					salida+= "\nFecha Ultima Factura: "+ str(reporte._lastInvoiceDate)
					salida+= "\nHora Ultima Factura: "+ str(reporte._lastInvoiceTime)
					salida+= "\nNumero Ultima Nota de Debito: "+ str(reporte._numberOfLastDebitNote)
					salida+= "\nNumero Ultima Nota de Credito: "+ str(reporte._numberOfLastCreditNote)
					salida+= "\nNumero Ultimo Doc No Fiscal: "+ str(reporte._numberOfLastNonFiscal)
					salida+= "\nVentas Exento: "+ str(reporte._freeSalesTax)
					salida+= "\nBase Imponible Ventas IVA G: "+ str(reporte._generalRate1Sale)
					salida+= "\nImpuesto IVA G: "+ str(reporte._generalRate1Tax)
					salida+= "\nBase Imponible Ventas IVA R: "+ str(reporte._reducedRate2Sale)
					salida+= "\nImpuesto IVA R: "+ str(reporte._reducedRate2Tax)
					salida+= "\nBase Imponible Ventas IVA A: "+ str(reporte._additionalRate3Sal)
					salida+= "\nImpuesto IVA A: "+ str(reporte._additionalRate3Tax)
					salida+= "\nPercibido en Ventas: "+ str(reporte._persivSales)
					salida+= "\nIGTF BI IVA en Ventas: "+ str(reporte._igtfRateSales)
					salida+= "\nImpuesto IGTF IVA en Ventas: "+ str(reporte._igtfRateTaxSales)
					salida+= "\nNota de Debito Exento: "+ str(reporte._freeTaxDebit)
					salida+= "\nBI IVA G en Nota de Debito: "+ str(reporte._generalRateDebit)
					salida+= "\nImpuesto IVA G en Nota de Debito: "+ str(reporte._generalRateTaxDebit)
					salida+= "\nBI IVA R en Nota de Debito: "+ str(reporte._reducedRateDebit)
					salida+= "\nImpuesto IVA R en Nota de Debito: "+ str(reporte._reducedRateTaxDebit)
					salida+= "\nBI IVA A en Nota de Debito: "+ str(reporte._additionalRateDebit)
					salida+= "\nImpuesto IVA A en Nota de Debito: "+ str(reporte._additionalRateTaxDebit)
					salida+= "\nPercibido en Debito: "+ str(reporte._persivDebit)
					salida+= "\nIGTF BI IVA en Nota de Debito: "+ str(reporte._igtfRateDebit)
					salida+= "\nImpuesto IGTF IVA en Nota de Debito: "+ str(reporte._igtfRateTaxDebit)
					salida+= "\nNota de Credito Exento: "+ str(reporte._freeTaxDevolution)
					salida+= "\nBI IVA G en Nota de Credito: "+ str(reporte._generalRateDevolution)
					salida+= "\nImpuesto IVA G en Nota de Credito: "+ str(reporte._generalRateTaxDevolution)
					salida+= "\nBI IVA R en Nota de Credito: "+ str(reporte._reducedRateDevolution)
					salida+= "\nImpuesto IVA R en Nota de Credito: "+ str(reporte._reducedRateTaxDevolution)
					salida+= "\nBI IVA A en Nota de Credito: "+ str(reporte._additionalRateDevolution)
					salida+= "\nImpuesto IVA A en Nota de Credito: "+ str(reporte._additionalRateTaxDevolution)
					salida+= "\nPercibido en Nota de Credito: "+ str(reporte._persivDevolution)
					salida+= "\nIGTF BI IVA A en Nota de Credito: "+ str(reporte._igtfRateDevolution)
					salida+= "\nImpuesto IGTF A en Nota de Credito: "+ str(reporte._igtfRateTaxDevolution)
					self.txt_informacion.setText(salida)
					if reporte:
						self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
						self.ver_con.setText("Leer Ult. Rep. Z")
				except:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
					self.ver_con.setText("Ult. Rep. Z")		
					self.txt_informacion.setText("No se pudo procesar el comando. Por favor valide estado y error de la impresora.")			
		else:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Ult. Rep. Z")		
			self.txt_informacion.setText("Impresora No Conectada")						

	def obtener_reporteX(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Obt. Reporte X")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:
			try:							
				reporte = self.printer.GetXReport()
				salida= "---EXTRACCIÓN DE REPORTE X---\n"
				salida+= "\nNumero Proximo Reporte Z: "+ str(reporte._numberOfLastZReport)
				salida+= "\nFecha Ultimo Reporte Z: "+ str(reporte._zReportDate)
				salida+= "\nHora Ultimo Reporte Z: "+ str(reporte._zReportTime)
				salida+= "\nNumero Ultima Factura: "+ str(reporte._numberOfLastInvoice)
				salida+= "\nFecha Ultima Factura: "+ str(reporte._lastInvoiceDate)
				salida+= "\nHora Ultima Factura: "+ str(reporte._lastInvoiceTime)
				salida+= "\nNumero Ultima Nota de Debito: "+ str(reporte._numberOfLastDebitNote)
				salida+= "\nNumero Ultima Nota de Credito: "+ str(reporte._numberOfLastCreditNote)
				salida+= "\nNumero Ultimo Doc No Fiscal: "+ str(reporte._numberOfLastNonFiscal)
				salida+= "\nVentas Exento: "+ str(reporte._freeSalesTax)
				salida+= "\nBase Imponible Ventas IVA G: "+ str(reporte._generalRate1Sale)
				salida+= "\nImpuesto IVA G: "+ str(reporte._generalRate1Tax)
				salida+= "\nBase Imponible Ventas IVA R: "+ str(reporte._reducedRate2Sale)
				salida+= "\nImpuesto IVA R: "+ str(reporte._reducedRate2Tax)
				salida+= "\nBase Imponible Ventas IVA A: "+ str(reporte._additionalRate3Sal)
				salida+= "\nImpuesto IVA A: "+ str(reporte._additionalRate3Tax)
				salida+= "\nPercibido en Ventas: "+ str(reporte._persivSales)
				salida+= "\nIGTF BI IVA en Ventas: "+ str(reporte._igtfRateSales)
				salida+= "\nImpuesto IGTF IVA en Ventas: "+ str(reporte._igtfRateTaxSales)
				salida+= "\nNota de Debito Exento: "+ str(reporte._freeTaxDebit)
				salida+= "\nBI IVA G en Nota de Debito: "+ str(reporte._generalRateDebit)
				salida+= "\nImpuesto IVA G en Nota de Debito: "+ str(reporte._generalRateTaxDebit)
				salida+= "\nBI IVA R en Nota de Debito: "+ str(reporte._reducedRateDebit)
				salida+= "\nImpuesto IVA R en Nota de Debito: "+ str(reporte._reducedRateTaxDebit)
				salida+= "\nBI IVA A en Nota de Debito: "+ str(reporte._additionalRateDebit)
				salida+= "\nImpuesto IVA A en Nota de Debito: "+ str(reporte._additionalRateTaxDebit)
				salida+= "\nPercibido en Debito: "+ str(reporte._persivDebit)
				salida+= "\nIGTF BI IVA en Nota de Debito: "+ str(reporte._igtfRateDebit)
				salida+= "\nImpuesto IGTF IVA en Nota de Debito: "+ str(reporte._igtfRateTaxDebit)
				salida+= "\nNota de Credito Exento: "+ str(reporte._freeTaxDevolution)
				salida+= "\nBI IVA G en Nota de Credito: "+ str(reporte._generalRateDevolution)
				salida+= "\nImpuesto IVA G en Nota de Credito: "+ str(reporte._generalRateTaxDevolution)
				salida+= "\nBI IVA R en Nota de Credito: "+ str(reporte._reducedRateDevolution)
				salida+= "\nImpuesto IVA R en Nota de Credito: "+ str(reporte._reducedRateTaxDevolution)
				salida+= "\nBI IVA A en Nota de Credito: "+ str(reporte._additionalRateDevolution)
				salida+= "\nImpuesto IVA A en Nota de Credito: "+ str(reporte._additionalRateTaxDevolution)
				salida+= "\nPercibido en Nota de Credito: "+ str(reporte._persivDevolution)
				salida+= "\nIGTF BI IVA A en Nota de Credito: "+ str(reporte._igtfRateDevolution)
				salida+= "\nImpuesto IGTF A en Nota de Credito: "+ str(reporte._igtfRateTaxDevolution)
				
				self.txt_informacion.setText(salida)
				if reporte:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
					self.ver_con.setText("Leer Rep. X")
			except:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
				self.ver_con.setText("Leer Reporte X")		
				self.txt_informacion.setText("No se pudo procesar el comando. Por favor valide estado y error de la impresora.")										

	def reporte_archivo (self):
		report = str(self.rep_r.currentText())	
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Reporte a Archivo")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:
			if report == "U0Z":
				try:
					reporte = self.printer.GetZReport()
					salida= "---EXTRACCIÓN DE REPORTE Z---\n"
					salida+= "\nNumero Ultimo Reporte Z: "+ str(reporte._numberOfLastZReport)
					salida+= "\nFecha Ultimo Reporte Z: "+ str(reporte._zReportDate)
					salida+= "\nHora Ultimo Reporte Z: "+ str(reporte._zReportTime)
					salida+= "\nNumero Ultima Factura: "+ str(reporte._numberOfLastInvoice)
					salida+= "\nFecha Ultima Factura: "+ str(reporte._lastInvoiceDate)
					salida+= "\nHora Ultima Factura: "+ str(reporte._lastInvoiceTime)
					salida+= "\nNumero Ultima Nota de Debito: "+ str(reporte._numberOfLastDebitNote)
					salida+= "\nNumero Ultima Nota de Credito: "+ str(reporte._numberOfLastCreditNote)
					salida+= "\nNumero Ultimo Doc No Fiscal: "+ str(reporte._numberOfLastNonFiscal)
					salida+= "\nVentas Exento: "+ str(reporte._freeSalesTax)
					salida+= "\nBase Imponible Ventas IVA G: "+ str(reporte._generalRate1Sale)
					salida+= "\nImpuesto IVA G: "+ str(reporte._generalRate1Tax)
					salida+= "\nBase Imponible Ventas IVA R: "+ str(reporte._reducedRate2Sale)
					salida+= "\nImpuesto IVA R: "+ str(reporte._reducedRate2Tax)
					salida+= "\nBase Imponible Ventas IVA A: "+ str(reporte._additionalRate3Sal)
					salida+= "\nImpuesto IVA A: "+ str(reporte._additionalRate3Tax)
					salida+= "\nPercibido en Ventas: "+ str(reporte._persivSales)
					salida+= "\nIGTF BI IVA en Ventas: "+ str(reporte._igtfRateSales)
					salida+= "\nImpuesto IGTF IVA en Ventas: "+ str(reporte._igtfRateTaxSales)
					salida+= "\nNota de Debito Exento: "+ str(reporte._freeTaxDebit)
					salida+= "\nBI IVA G en Nota de Debito: "+ str(reporte._generalRateDebit)
					salida+= "\nImpuesto IVA G en Nota de Debito: "+ str(reporte._generalRateTaxDebit)
					salida+= "\nBI IVA R en Nota de Debito: "+ str(reporte._reducedRateDebit)
					salida+= "\nImpuesto IVA R en Nota de Debito: "+ str(reporte._reducedRateTaxDebit)
					salida+= "\nBI IVA A en Nota de Debito: "+ str(reporte._additionalRateDebit)
					salida+= "\nImpuesto IVA A en Nota de Debito: "+ str(reporte._additionalRateTaxDebit)
					salida+= "\nPercibido en Debito: "+ str(reporte._persivDebit)
					salida+= "\nIGTF BI IVA en Nota de Debito: "+ str(reporte._igtfRateDebit)
					salida+= "\nImpuesto IGTF IVA en Nota de Debito: "+ str(reporte._igtfRateTaxDebit)
					salida+= "\nNota de Credito Exento: "+ str(reporte._freeTaxDevolution)
					salida+= "\nBI IVA G en Nota de Credito: "+ str(reporte._generalRateDevolution)
					salida+= "\nImpuesto IVA G en Nota de Credito: "+ str(reporte._generalRateTaxDevolution)
					salida+= "\nBI IVA R en Nota de Credito: "+ str(reporte._reducedRateDevolution)
					salida+= "\nImpuesto IVA R en Nota de Credito: "+ str(reporte._reducedRateTaxDevolution)
					salida+= "\nBI IVA A en Nota de Credito: "+ str(reporte._additionalRateDevolution)
					salida+= "\nImpuesto IVA A en Nota de Credito: "+ str(reporte._additionalRateTaxDevolution)
					salida+= "\nPercibido en Nota de Credito: "+ str(reporte._persivDevolution)
					salida+= "\nIGTF BI IVA A en Nota de Credito: "+ str(reporte._igtfRateDevolution)
					salida+= "\nImpuesto IGTF A en Nota de Credito: "+ str(reporte._igtfRateTaxDevolution)
					if reporte:
						self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
						self.ver_con.setText("Leer Ult. Rep. Z")
				except:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
					self.ver_con.setText("Ult. Rep. Z a Archivo")
					salida="No se pudo extraer informacion..."
			
			if report == "U0X":
				try:
					reporte = self.printer.GetXReport()
					salida= "---EXTRACCIÓN DE REPORTE X---\n"
					salida+= "\nNumero Proximo Reporte Z: "+ str(reporte._numberOfLastZReport)
					salida+= "\nFecha Ultimo Reporte Z: "+ str(reporte._zReportDate)
					salida+= "\nHora Ultimo Reporte Z: "+ str(reporte._zReportTime)
					salida+= "\nNumero Ultima Factura: "+ str(reporte._numberOfLastInvoice)
					salida+= "\nFecha Ultima Factura: "+ str(reporte._lastInvoiceDate)
					salida+= "\nHora Ultima Factura: "+ str(reporte._lastInvoiceTime)
					salida+= "\nNumero Ultima Nota de Debito: "+ str(reporte._numberOfLastDebitNote)
					salida+= "\nNumero Ultima Nota de Credito: "+ str(reporte._numberOfLastCreditNote)
					salida+= "\nNumero Ultimo Doc No Fiscal: "+ str(reporte._numberOfLastNonFiscal)
					salida+= "\nVentas Exento: "+ str(reporte._freeSalesTax)
					salida+= "\nBase Imponible Ventas IVA G: "+ str(reporte._generalRate1Sale)
					salida+= "\nImpuesto IVA G: "+ str(reporte._generalRate1Tax)
					salida+= "\nBase Imponible Ventas IVA R: "+ str(reporte._reducedRate2Sale)
					salida+= "\nImpuesto IVA R: "+ str(reporte._reducedRate2Tax)
					salida+= "\nBase Imponible Ventas IVA A: "+ str(reporte._additionalRate3Sal)
					salida+= "\nImpuesto IVA A: "+ str(reporte._additionalRate3Tax)
					salida+= "\nPercibido en Ventas: "+ str(reporte._persivSales)
					salida+= "\nIGTF BI IVA en Ventas: "+ str(reporte._igtfRateSales)
					salida+= "\nImpuesto IGTF IVA en Ventas: "+ str(reporte._igtfRateTaxSales)
					salida+= "\nNota de Debito Exento: "+ str(reporte._freeTaxDebit)
					salida+= "\nBI IVA G en Nota de Debito: "+ str(reporte._generalRateDebit)
					salida+= "\nImpuesto IVA G en Nota de Debito: "+ str(reporte._generalRateTaxDebit)
					salida+= "\nBI IVA R en Nota de Debito: "+ str(reporte._reducedRateDebit)
					salida+= "\nImpuesto IVA R en Nota de Debito: "+ str(reporte._reducedRateTaxDebit)
					salida+= "\nBI IVA A en Nota de Debito: "+ str(reporte._additionalRateDebit)
					salida+= "\nImpuesto IVA A en Nota de Debito: "+ str(reporte._additionalRateTaxDebit)
					salida+= "\nPercibido en Debito: "+ str(reporte._persivDebit)
					salida+= "\nIGTF BI IVA en Nota de Debito: "+ str(reporte._igtfRateDebit)
					salida+= "\nImpuesto IGTF IVA en Nota de Debito: "+ str(reporte._igtfRateTaxDebit)
					salida+= "\nNota de Credito Exento: "+ str(reporte._freeTaxDevolution)
					salida+= "\nBI IVA G en Nota de Credito: "+ str(reporte._generalRateDevolution)
					salida+= "\nImpuesto IVA G en Nota de Credito: "+ str(reporte._generalRateTaxDevolution)
					salida+= "\nBI IVA R en Nota de Credito: "+ str(reporte._reducedRateDevolution)
					salida+= "\nImpuesto IVA R en Nota de Credito: "+ str(reporte._reducedRateTaxDevolution)
					salida+= "\nBI IVA A en Nota de Credito: "+ str(reporte._additionalRateDevolution)
					salida+= "\nImpuesto IVA A en Nota de Credito: "+ str(reporte._additionalRateTaxDevolution)
					salida+= "\nPercibido en Nota de Credito: "+ str(reporte._persivDevolution)
					salida+= "\nIGTF BI IVA A en Nota de Credito: "+ str(reporte._igtfRateDevolution)
					salida+= "\nImpuesto IGTF A en Nota de Credito: "+ str(reporte._igtfRateTaxDevolution)
					if reporte:
						self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
						self.ver_con.setText("Leer Rep. X")
				except:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
					self.ver_con.setText("Rep. X a Archivo")
					salida="No se pudo extraer informacion..."	
											
			root = tk.Tk()
			root.withdraw()
			nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
			if nombre_archivo:
				# Abre el archivo en modo de escritura ('w')
				with open(nombre_archivo, 'w') as archivo:
					# Escribe cada línea en el archivo
					for linea in salida:
						archivo.write(linea)  # Agrega un salto de línea al final de cada línea
				print(f"Se ha guardado el archivo en: {nombre_archivo}")
			else:
				print("No se ha seleccionado ninguna ubicación para guardar el archivo.")

	def ImpZpornumero(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Imp. Z por Num.")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			n_ini = self.imp_num_ini.value()
			n_fin = self.imp_num_fin.value()
			trama_repz = self.printer.PrintZReport("A",n_ini,n_fin)
			contador = 1
			while trama_repz == None and contador < 6:
				time.sleep(1)
				contador += 1			
			match trama_repz:
				case _:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Imp. Z por Num.")


	def ImpZporfecha(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Imp. Z por Fecha")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:					
			n_ini = self.imp_date_ini.date().toPyDate()
			n_fin = self.imp_date_fin.date().toPyDate()
			trama_repz = self.printer.PrintZReport("A",n_ini,n_fin)
			contador = 1
			while trama_repz == None and contador < 6:
				time.sleep(1)
				contador += 1
			match trama_repz:
				case _:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 9pt;")
					self.ver_con.setText("Imp. Z por Fecha")		

				

	def factura(self):
		#Factura sin Personalizar*
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Factura Simple")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:			
			self.printer.SendCmd(str("PJ5000"))
			self.printer.SendCmd(str("@COMMENT/COMENTARIO"))
			self.printer.SendCmd(str(" 000000030000001000Tax Free/Producto Exento"))
			self.printer.SendCmd(str("!000000050000001000Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str('"' + "000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("#000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
			subt = self.printer.SendCmd(str("3"))
			self.printer.SendCmd(str("101"))
			time.sleep (1)												# Esperar para verificar estado booleano de comando
			if subt:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
				self.ver_con.setText("Factura Simple")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
				self.ver_con.setText("Factura Simple")			

	def facturaper(self):
		#Factura Personalizada
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Fact. Personalizada")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			self.printer.SendCmd(str("PJ5000"))
			self.printer.SendCmd(str("iR*21.122.012"))
			self.printer.SendCmd(str("iS*Pedro Perez"))
			self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
			self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
			self.printer.SendCmd(str("i02CAJERO: 00001"))
			self.printer.SendCmd(str("@COMMENT/COMENTARIO"))
			self.printer.SendCmd(str(" 000000030000001000Tax Free/Producto Exento"))
			self.printer.SendCmd(str("!000000050000001000Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str('"' + "000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("#000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
			subt = self.printer.SendCmd(str("3"))
			self.printer.SendCmd(str("201000000001000"))
			self.printer.SendCmd(str("101"))
			#self.printer.SendCmd(str("199"))
			time.sleep (1)												# Esperar para verificar estado booleano de comando		
			if subt:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
				self.ver_con.setText("Fact. Personalizada")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
				self.ver_con.setText("Fact. Personalizada")				
		
#	def facturaperc(self):
#		#Factura con Percibido
#		#self.printer.SendCmd(str("PJ5001"))
#		self.printer.SendCmd(str("iR*21.122.012"))
#		self.printer.SendCmd(str("iS*Pedro Perez"))
#		self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
#		self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
#		self.printer.SendCmd(str("i02CAJERO: 00001"))
#		self.printer.SendCmd(str("@COMMENT/COMENTARIO"))
#		self.printer.SendCmd(str(" 000000030000001000Tax Free/Producto Exento"))
#		self.printer.SendCmd(str("!000000050000001000Tax Rate 1/Producto Tasa General"))
#		self.printer.SendCmd(str('"' + "000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
#		self.printer.SendCmd(str("#000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
#		self.printer.SendCmd(str("$000000090000001000Tax Rate 4/ Producto Tasa Percibido"))
#		self.printer.SendCmd(str("3"))
#		self.printer.SendCmd(str("201000000001000"))
#		self.printer.SendCmd(str("101"))
		#self.printer.SendCmd(str("199"))
	
	def facturaigtf(self):
		#Factura con IGTF
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Factura IGTF")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			self.printer.SendCmd(str("PJ5001"))
			self.printer.SendCmd(str("iR*21.122.012"))
			self.printer.SendCmd(str("iS*Pedro Perez"))
			self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
			self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
			self.printer.SendCmd(str("i02CAJERO: 00001"))
			self.printer.SendCmd(str("@COMMENT/COMENTARIO"))
			self.printer.SendCmd(str(" 000000030000001000Tax Free/Producto Exento"))
			self.printer.SendCmd(str("!000000050000001000Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str('"' + "000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("#000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
			self.printer.SendCmd(str("$000000090000001000Tax Rate 4/ Producto Tasa Percibido"))
			subt = self.printer.SendCmd(str("3"))
			self.printer.SendCmd(str("224000000001000"))
			self.printer.SendCmd(str("101"))
			self.printer.SendCmd(str("199"))
			time.sleep (2)												# Esperar para verificar estado booleano de comando		
			if subt:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
				self.ver_con.setText("Factura IGTF")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
				self.ver_con.setText("Factura IGTF")				

	def facturaanu(self):
		#Factura Anulada
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Factura Anulada")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			self.printer.SendCmd(str("iR*21.122.012"))
			self.printer.SendCmd(str("iS*Pedro Perez"))
			self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
			self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
			self.printer.SendCmd(str("i02CAJERO: 00001"))
			self.printer.SendCmd(str("@COMMENT/COMENTARIO"))
			self.printer.SendCmd(str(" 000000030000001000Tax Free/Producto Exento"))
			self.printer.SendCmd(str("!000000050000001000Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str('"' + "000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("#000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
			anula_fac = self.printer.SendCmd(str("7"))
			time.sleep (2)												# Esperar para verificar estado booleano de comando
			if anula_fac:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
				self.ver_con.setText("Factura Anulada")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
				self.ver_con.setText("Factura Anulada")				

	def documentoNF(self):
		#Documento No Fiscal
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Doc. No Fiscal")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			self.printer.SendCmd(str("80$Documento de Prueba"))
			self.printer.SendCmd(str("80¡Esto es un documento de texto"))
			self.printer.SendCmd(str("80!Es un documento no fiscal"))
			self.printer.SendCmd(str("80*Es bastante util y versatil"))
			cierre_dnf = self.printer.SendCmd(str("810Fin del Documento no Fiscal"))
			time.sleep (1)												# Esperar para verificar estado booleano de comando
			if cierre_dnf:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
				self.ver_con.setText("Doc. no Fiscal")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
				self.ver_con.setText("Doc. no Fiscal")				

	def notaCredito(self):
		#Nota de Credito
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Nota de Credito")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			self.printer.SendCmd(str("PJ5000"))
			self.printer.SendCmd(str("iR*21.122.012"))
			self.printer.SendCmd(str("iS*Pedro Perez"))
			self.printer.SendCmd(str("iF*00000000001"))
			self.printer.SendCmd(str("iD*22/08/2016"))
			self.printer.SendCmd(str("iI*Z1F1234567"))
			self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
			self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
			self.printer.SendCmd(str("i02CAJERO: 00001"))
			self.printer.SendCmd(str("ACOMENTARIO NOTA DE CREDITO"))
			self.printer.SendCmd(str("d0000000030000001000Tax Free/Producto Exento"))
			self.printer.SendCmd(str("d1000000050000001000Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str("d2000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("d3000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
			subt = self.printer.SendCmd(str("3"))
			self.printer.SendCmd(str("101"))								
			time.sleep (1)												# Esperar para verificar estado booleano de comando		
			if subt:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
				self.ver_con.setText("Nota de Credito")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
				self.ver_con.setText("Nota de Credito")				
	
	def notaCreditoIgtf(self):
		#Nota de Credito con IGTF
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Nota Cred. IGTF")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:				
			self.printer.SendCmd(str("PJ5001"))
			self.printer.SendCmd(str("iR*21.122.012"))
			self.printer.SendCmd(str("iS*Pedro Perez"))
			self.printer.SendCmd(str("iF*00000000001"))
			self.printer.SendCmd(str("iD*22/08/2016"))
			self.printer.SendCmd(str("iI*Z1F1234567"))
			self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
			self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
			self.printer.SendCmd(str("i02CAJERO: 00001"))
			self.printer.SendCmd(str("ACOMENTARIO NOTA DE CREDITO"))
			self.printer.SendCmd(str("d0000000030000001000Tax Free/Producto Exento"))
			self.printer.SendCmd(str("d1000000050000001000Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str("d2000000070000001000Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("d3000000090000001000Tax Rate 3/ Producto Tasa Adicional"))
			self.printer.SendCmd(str("224000000001000"))
			cierre_notacredigtf = self.printer.SendCmd(str("101"))
			self.printer.SendCmd(str("199"))
			time.sleep (1)												# Esperar para verificar estado booleano de comando
			if cierre_notacredigtf:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 7pt;")
				self.ver_con.setText("Nota de Cred. IGTF")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
				self.ver_con.setText("Nota de Cred. IGTF")					

	def notaDebito(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Nota de Debito")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:					
			self.printer.SendCmd(str("PJ5000"))
			self.printer.SendCmd(str("iR*21.122.012"))
			self.printer.SendCmd(str("iS*Pedro Perez"))
			self.printer.SendCmd(str("iF*00000000001"))
			self.printer.SendCmd(str("iD*22/08/2016"))
			self.printer.SendCmd(str("iI*Z1F1234567"))
			self.printer.SendCmd(str("i00Direccion: Ppal Siempre Viva"))
			self.printer.SendCmd(str("i01Telefono: +58(212)555-55-55"))
			self.printer.SendCmd(str("i02CAJERO: 00001"))
			self.printer.SendCmd(str("BCOMENTARIO NOTA DE DEBITO"))
			self.printer.SendCmd(str("`0" + "000000003000000100Tax Free/Producto Exento"))
			self.printer.SendCmd(str("`1" + "100000005000000100Tax Rate 1/Producto Tasa General"))
			self.printer.SendCmd(str("`2" + "200000007000000100Tax Rate 2/ Producto Tasa Reducida"))
			self.printer.SendCmd(str("`3" + "300000009000000100Tax Rate 3/ Producto Tasa Adicional"))
			subt = self.printer.SendCmd(str("3"))
			self.printer.SendCmd(str("101"))
			time.sleep (1)												# Esperar para verificar estado booleano de comando
			if subt:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
				self.ver_con.setText("Nota de Debito")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
				self.ver_con.setText("Nota de Debito")					

	def ReimprimirFacturas(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Reimp. Fact.")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:		
			n_ini = self.reimp_ini.value()
			n_fin = self.reimp_fin.value()

			starString = str(n_ini)
			while (len(starString) < 7):
				starString = "0" + starString
			endString = str(n_fin)
			while (len(endString) < 7):
				endString = "0" + endString
			reimpfac = self.printer.SendCmd("RF" + starString + endString)
			time.sleep (1)												# Esperar para verificar estado booleano de comando
			if reimpfac:
				self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
				self.ver_con.setText("Reimp. Fact.")
			else:
				self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
			self.ver_con.setText("Reimp. Fact.")					

	def ObtFactpornumero (self):
		print ("Comando no existe en libreria...")


	def ObtZpornumero(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Obt. Z Por Num.")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:			
			n_ini = self.obt_num_ini.value()
			n_fin = self.obt_num_fin.value()
			try:
				reportes = self.printer.GetZReport("A",n_ini,n_fin)
				CR = len(reportes)
				Enc = "Lista de Reportes Por Número\n"+"\n"
				salida = ""
				for NR in range(CR):
					salida+= "Numero de Reporte Z: "+ str(reportes[NR]._numberOfLastZReport)
					salida+= "\nFecha Ultimo Reporte Z: "+ str(reportes[NR]._zReportDate)
					salida+= "\nHora Ultimo Reporte Z: "+ str(reportes[NR]._zReportTime)
					salida+= "\nNumero Ultima Factura: "+ str(reportes[NR]._numberOfLastInvoice)
					salida+= "\nFecha Ultima Factura: "+ str(reportes[NR]._lastInvoiceDate)
					salida+= "\nHora Ultima Factura: "+ str(reportes[NR]._lastInvoiceTime)
					salida+= "\nNumero Ultima Nota de Credito: "+ str(reportes[NR]._numberOfLastCreditNote)
					salida+= "\nNumero Ultima Nota de Debito: "+ str(reportes[NR]._numberOfLastDebitNote)
					salida+= "\nNumero Ultimo Doc No Fiscal: "+ str(reportes[NR]._numberOfLastNonFiscal)
					salida+= "\nVentas Exento: "+ str(reportes[NR]._freeSalesTax)
					salida+= "\nBase Imponible Ventas IVA G: "+ str(reportes[NR]._generalRate1Sale)
					salida+= "\nImpuesto IVA G: "+ str(reportes[NR]._generalRate1Tax)
					salida+= "\nBase Imponible Ventas IVA R: "+ str(reportes[NR]._reducedRate2Sale)
					salida+= "\nImpuesto IVA R: "+ str(reportes[NR]._reducedRate2Tax)
					salida+= "\nBase Imponible Ventas IVA A: "+ str(reportes[NR]._additionalRate3Sal)
					salida+= "\nImpuesto IVA A: "+ str(reportes[NR]._additionalRate3Tax)
					salida+= "\nPercibido en Ventas: "+ str(reportes[NR]._persivSales)
					salida+= "\nIGTF BI IVA en Ventas: "+ str(reportes[NR]._igtfRateSales)
					salida+= "\nImpuesto IGTF IVA en Ventas: "+ str(reportes[NR]._igtfRateTaxSales)
					salida+= "\nNota de Debito Exento: "+ str(reportes[NR]._freeTaxDebit)
					salida+= "\nBI IVA G en Nota de Debito: "+ str(reportes[NR]._generalRateDebit)
					salida+= "\nImpuesto IVA G en Nota de Debito: "+ str(reportes[NR]._generalRateTaxDebit)
					salida+= "\nBI IVA R en Nota de Debito: "+ str(reportes[NR]._reducedRateDebit)
					salida+= "\nImpuesto IVA R en Nota de Debito: "+ str(reportes[NR]._reducedRateTaxDebit)
					salida+= "\nBI IVA A en Nota de Debito: "+ str(reportes[NR]._additionalRateDebit)
					salida+= "\nImpuesto IVA A en Nota de Debito: "+ str(reportes[NR]._additionalRateTaxDebit)
					salida+= "\nPercibido en Debito: "+ str(reportes[NR]._persivDebit)
					salida+= "\nIGTF BI IVA en Nota de Debito: "+ str(reportes[NR]._igtfRateDebit)
					salida+= "\nImpuesto IGTF IVA en Nota de Debito: "+ str(reportes[NR]._igtfRateTaxDebit)
					salida+= "\nNota de Credito Exento: "+ str(reportes[NR]._freeTaxDevolution)
					salida+= "\nBI IVA G en Nota de Credito: "+ str(reportes[NR]._generalRateDevolution)
					salida+= "\nImpuesto IVA G en Nota de Credito: "+ str(reportes[NR]._generalRateTaxDevolution)
					salida+= "\nBI IVA R en Nota de Credito: "+ str(reportes[NR]._reducedRateDevolution)
					salida+= "\nImpuesto IVA R en Nota de Credito: "+ str(reportes[NR]._reducedRateTaxDevolution)
					salida+= "\nBI IVA A en Nota de Credito: "+ str(reportes[NR]._additionalRateDevolution)
					salida+= "\nImpuesto IVA A en Nota de Credito: "+ str(reportes[NR]._additionalRateTaxDevolution)
					salida+= "\nPercibido en Nota de Credito: "+ str(reportes[NR]._persivDevolution)
					salida+= "\nIGTF BI IVA A en Nota de Credito: "+ str(reportes[NR]._igtfRateDevolution)
					salida+= "\nImpuesto IGTF A en Nota de Credito: "+ str(reportes[NR]._igtfRateTaxDevolution)+"\n"+"\n"
				self.txt_informacion.setText(Enc+salida)
				time.sleep (1)												# Esperar para verificar estado booleano de comando		
				if salida:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
					self.ver_con.setText("Obt. Z por Num")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
					self.ver_con.setText("Obt. Z por Num")	
			except:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
					self.ver_con.setText("Obt. Z por Num")		
					self.txt_informacion.setText("No se pudo procesar el comando. Por favor valide estado y error de la impresora.")					

	def ObtZporfecha(self):
		if not self.printer.bandera:
			self.ver_con.setStyleSheet("background-color: yellow;color: black;font: 900 7pt")
			self.ver_con.setText("Obt. Z Por Fecha")		
			self.txt_informacion.setText("Impresora No Conectada")
		else:						
			n_ini = self.obt_date_ini.date().toPyDate()
			n_fin = self.obt_date_fin.date().toPyDate()
			try:
				reportes = self.printer.GetZReport("A",n_ini,n_fin)
				CR = len(reportes)
				Enc = "Lista de Reportes Por Rango de Fechas\n"+"\n"
				salida = ""
				for NR in range(CR):
					salida+= "Numero de Reporte Z: "+ str(reportes[NR]._numberOfLastZReport)
					salida+= "\nFecha Ultimo Reporte Z: "+ str(reportes[NR]._zReportDate)
					salida+= "\nHora Ultimo Reporte Z: "+ str(reportes[NR]._zReportTime)
					salida+= "\nNumero Ultima Factura: "+ str(reportes[NR]._numberOfLastInvoice)
					salida+= "\nFecha Ultima Factura: "+ str(reportes[NR]._lastInvoiceDate)
					salida+= "\nHora Ultima Factura: "+ str(reportes[NR]._lastInvoiceTime)
					salida+= "\nNumero Ultima Nota de Credito: "+ str(reportes[NR]._numberOfLastCreditNote)
					salida+= "\nNumero Ultima Nota de Debito: "+ str(reportes[NR]._numberOfLastDebitNote)
					salida+= "\nNumero Ultimo Doc No Fiscal: "+ str(reportes[NR]._numberOfLastNonFiscal)
					salida+= "\nVentas Exento: "+ str(reportes[NR]._freeSalesTax)
					salida+= "\nBase Imponible Ventas IVA G: "+ str(reportes[NR]._generalRate1Sale)
					salida+= "\nImpuesto IVA G: "+ str(reportes[NR]._generalRate1Tax)
					salida+= "\nBase Imponible Ventas IVA R: "+ str(reportes[NR]._reducedRate2Sale)
					salida+= "\nImpuesto IVA R: "+ str(reportes[NR]._reducedRate2Tax)
					salida+= "\nBase Imponible Ventas IVA A: "+ str(reportes[NR]._additionalRate3Sal)
					salida+= "\nImpuesto IVA A: "+ str(reportes[NR]._additionalRate3Tax)
					salida+= "\nPercibido en Ventas: "+ str(reportes[NR]._persivSales)
					salida+= "\nIGTF BI IVA en Ventas: "+ str(reportes[NR]._igtfRateSales)
					salida+= "\nImpuesto IGTF IVA en Ventas: "+ str(reportes[NR]._igtfRateTaxSales)
					salida+= "\nNota de Debito Exento: "+ str(reportes[NR]._freeTaxDebit)
					salida+= "\nBI IVA G en Nota de Debito: "+ str(reportes[NR]._generalRateDebit)
					salida+= "\nImpuesto IVA G en Nota de Debito: "+ str(reportes[NR]._generalRateTaxDebit)
					salida+= "\nBI IVA R en Nota de Debito: "+ str(reportes[NR]._reducedRateDebit)
					salida+= "\nImpuesto IVA R en Nota de Debito: "+ str(reportes[NR]._reducedRateTaxDebit)
					salida+= "\nBI IVA A en Nota de Debito: "+ str(reportes[NR]._additionalRateDebit)
					salida+= "\nImpuesto IVA A en Nota de Debito: "+ str(reportes[NR]._additionalRateTaxDebit)
					salida+= "\nPercibido en Debito: "+ str(reportes[NR]._persivDebit)
					salida+= "\nIGTF BI IVA en Nota de Debito: "+ str(reportes[NR]._igtfRateDebit)
					salida+= "\nImpuesto IGTF IVA en Nota de Debito: "+ str(reportes[NR]._igtfRateTaxDebit)
					salida+= "\nNota de Credito Exento: "+ str(reportes[NR]._freeTaxDevolution)
					salida+= "\nBI IVA G en Nota de Credito: "+ str(reportes[NR]._generalRateDevolution)
					salida+= "\nImpuesto IVA G en Nota de Credito: "+ str(reportes[NR]._generalRateTaxDevolution)
					salida+= "\nBI IVA R en Nota de Credito: "+ str(reportes[NR]._reducedRateDevolution)
					salida+= "\nImpuesto IVA R en Nota de Credito: "+ str(reportes[NR]._reducedRateTaxDevolution)
					salida+= "\nBI IVA A en Nota de Credito: "+ str(reportes[NR]._additionalRateDevolution)
					salida+= "\nImpuesto IVA A en Nota de Credito: "+ str(reportes[NR]._additionalRateTaxDevolution)
					salida+= "\nPercibido en Nota de Credito: "+ str(reportes[NR]._persivDevolution)
					salida+= "\nIGTF BI IVA A en Nota de Credito: "+ str(reportes[NR]._igtfRateDevolution)
					salida+= "\nImpuesto IGTF A en Nota de Credito: "+ str(reportes[NR]._igtfRateTaxDevolution)+"\n"+"\n"
				self.txt_informacion.setText(Enc+salida)
				time.sleep (1)												# Esperar para verificar estado booleano de comando		
				if salida:
					self.ver_con.setStyleSheet("background-color: rgb(0, 227, 0);color: black;font: 900 8pt;")
					self.ver_con.setText("Obt. Z por Fecha")
				else:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 8pt")
					self.ver_con.setText("Obt. Z por Fecha")	
			except:
					self.ver_con.setStyleSheet("background-color: red;color: black;font: 900 7pt")
					self.ver_con.setText("Obt. Z por Fecha")		
					self.txt_informacion.setText("No se pudo procesar el comando. Por favor valide estado y error de la impresora.")	



	def status_description(self, status):
		match status:
			case "12":
				return 'En modo fiscal, carga completa de la memoria fiscal y emisión de documentos no fiscales'
			case "11":            
				return 'En modo fiscal, carga completa de la memoria fiscal y emisión de documentos fiscales'
			case "10":
				return 'En modo fiscal, carga completa de la memoria fiscal y en espera'
			case "9 ":
				return 'En modo fiscal, cercana carga completa de la memoria fiscal y en emisión de documentos no fiscales'
			case "8 ":
				return 'En modo fiscal, cercana carga completa de la memoria fiscal y en emisión de documentos no fiscales'
			case "7 ":
				return 'En modo fiscal, cercana carga completa de la memoria fiscal y en espera'
			case "6 ":
				return 'En modo fiscal y en emisión de documentos no fiscales'
			case "5 ":
				return 'En modo fiscal y en emisión de documentos fiscales'
			case "4 ":
				return 'En modo fiscal y en espera'
			case "3 ":
				return 'En modo prueba y en emisión de documentos no fiscales'
			case "2 ":
				return 'En modo prueba y en emisión de documentos fiscales'
			case "1 ":
				return 'En modo prueba y en espera'
			case "0 ":
				return 'Status Desconocido'
			case _:
				return 'Status Desconocido'  # Tratamiento por defecto													

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon("tfhka.jpg"))  	
	principal = Principal()
	principal.show()
	app.exec_()
