#!/usr/bin/env python
# coding: utf-8

# -------------------------------------------------------
import torch
import exgrads.hooks as hooks
def trH(model, x):
	model.eval()
	hooks.register(model)
	
	results = torch.zeros(x.shape[0])		# (b)
	results = results.to(x.device)

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
		del param.grad1

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
			del param.grad1
	
	hooks.deregister(model)
	return results


# -------------------------------------------------------

