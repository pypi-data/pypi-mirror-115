#!/usr/bin/env python
# coding: utf-8

# -------------------------------------------------------
import torch
import torch.nn.functional as F
import exgrads.hooks as hooks
def vectorize(model, x, y):
	model.eval()
	hooks.register(model)

	logit = model(x)
	loss  = F.cross_entropy(logit, y, reduction='sum')
	model.zero_grad()
	loss.backward()

	vectors = []
	for param in model.parameters():
		if not hasattr(param, 'grad1'): continue
		grad1 = param.grad1.detach()
		grad1 = grad1.flatten(1,-1)
		vectors.append(grad1)
		del param.grad1
	vectors = torch.cat(vectors,dim=1)

	hooks.deregister(model)
	return vectors


# -------------------------------------------------------
import torch
import torch.nn.functional as F
import exgrads.hooks as hooks
def normL2(model, x, y):
	model.eval()
	hooks.register(model)

	logit = model(x)
	loss  = F.cross_entropy(logit, y, reduction='sum')
	model.zero_grad()
	loss.backward()

	norms = torch.zeros(x.shape[0])
	norms = norms.to(x.device)

	for param in model.parameters():
		if not hasattr(param, 'grad1'): continue
		grad1 = param.grad1.detach()
		grad1 = grad1.flatten(1,-1)
		norms += grad1.pow(2).sum(dim=1)
		del param.grad1
	norms = norms.pow(0.5)
	
	hooks.deregister(model)
	return norms





# -------------------------------------------------------

