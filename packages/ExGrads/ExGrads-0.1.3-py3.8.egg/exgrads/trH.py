#!/usr/bin/env python
# coding: utf-8

__version__='0.1.2'
import torch

# -------------------------------------------------------
import exgrads.hooks as hooks
def trH(model, x, reduction='none'):
	results = torch.zeros(x.shape[0])

	model.eval()
	hooks.register(model)
	
	logit = model(x)								# := (b,K)

	# for p*p^T part
	Z		= torch.logsumexp(logit, dim=1)			# -> (b)
	loss 	= Z.sum()								# -> (1)
	
	loss.backward(retain_graph=True)
	model.zero_grad()
	for param in model.parameters():
		grad1 = param.grad1**2 						# := (b,*)
		grad1 = grad1.flatten(1,-1) 				# -> (b,prod(*))
		grad1 = torch.sum(grad1,dim=1) 				# -> (b,)
		results -= grad1.detach()

	# for diag(p) part
	prob	= torch.softmax(logit,dim=1)				# -> (b,K)
	prob	= prob.unsqueeze(dim=2)						# -> (b,K,1)
	logit	= logit.sum(dim=0)							# -> (K)
	for k, logit_k in enumerate(logit):
		logit_k.backward(retain_graph=True)
		model.zero_grad()
		for param in model.parameters():
			grad1 = param.grad1**2					# := (b,*)
			grad1 = grad1.flatten(1,-1)				# -> (b,prod(*))
			grad1 = prob[:,k] * grad1				# -> (b,prod(*))
			grad1 = grad1.flatten(1,-1)				# -> (b)
			grad1 = torch.sum(grad1,dim=1)			# -> (b)
			results += grad1.detach()

	if reduction=='sum':	results = torch.sum(results)
	if reduction=='mean':	results = torch.mean(results)
	
	hooks.deregister(model)
	return results


# -------------------------------------------------------

