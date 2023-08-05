
import asyncio
import logging
from aardwolf.commons.factory import RDPConnectionFactory
from aardwolf.commons.queuedata.constants import VIDEO_FORMAT
from aardwolf.commons.iosettings import RDPIOSettings
from asysocks.unicomm.common.scanner.targetgen import UniTargetGen
from asysocks.unicomm.common.scanner.scanner import UniScanner
from aardwolf import logger

from aardwolf.examples.scanners.rdplogin import RDPLoginScanner
from aardwolf.examples.scanners.rdpscaps import RDPCapabilitiesScanner
from aardwolf.examples.scanners.rdpscreen import RDPScreenshotScanner

rdpscan_options = {
	'login' : (RDPLoginScanner,'Checks if user can log in to hosts'),
	'caps'  : (RDPCapabilitiesScanner,'Lists RDP connection flags available'),
	'screen': (RDPScreenshotScanner,'Takes screenshot of the remote session'),
}

async def amain():
	import argparse

	scannertpes_usage = '\r\nall: Runs all scanners\r\n'
	for k in rdpscan_options:
		scannertpes_usage += '    %s: %s\r\n' % (k, rdpscan_options[k][1])
	
	usage = """
Scanner types (-s param):
    %s
"""% scannertpes_usage

	parser = argparse.ArgumentParser(description='RDP scanner', usage=usage)
	parser.add_argument('-w', '--worker-count', type=int, default=100, help='Parallell count')
	parser.add_argument('-t', '--timeout', type=int, default=10, help='Timeout for each connection')
	parser.add_argument('--no-progress', action='store_false', help='Disable progress bar')
	parser.add_argument('-o', '--out-file', help='Output file path.')
	parser.add_argument('-s', '--scan', action='append', required=True, help='Scanner type')
	parser.add_argument('-e', '--errors', action='store_true', help='Includes errors in output. It will mess up the formatting!')
	parser.add_argument('url', help = 'Connection string in URL format')
	parser.add_argument('targets', nargs='*', help = 'Hostname or IP address or file with a list of targets')
	args = parser.parse_args()

	if len(args.targets) == 0:
		print('No targets defined!')
		return
	
	logger.setLevel(logging.INFO)

	iosettings = RDPIOSettings()
	iosettings.channels = []
	iosettings.video_out_format = VIDEO_FORMAT.RAW
	iosettings.clipboard_use_pyperclip = False
	
	connectionfactory = RDPConnectionFactory.from_url(args.url, iosettings)
	scantypes = []
	for x in args.scan:
		scantypes.append(x.lower())
	executors = []
	if 'all' in scantypes:
		for k in rdpscan_options:
			executors.append(rdpscan_options[k][0](connectionfactory))
	else:
		for scantype in scantypes:
			if scantype not in rdpscan_options:
				print('Unknown scan type: "%s"' % scantype)
				return
			executors.append(rdpscan_options[scantype][0](connectionfactory))
		
	tgen = UniTargetGen.from_list(args.targets)
	scanner = UniScanner('RDPScanner', executors, [tgen], worker_count=args.worker_count, host_timeout=args.timeout)
	await scanner.scan_and_process(progress=args.no_progress, out_file=args.out_file, include_errors=args.errors)

def main():
	asyncio.run(amain())

if __name__ == '__main__':
	main()